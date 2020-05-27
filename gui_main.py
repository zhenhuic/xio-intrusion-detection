import os
import smtplib
import sys
import time
import datetime
import logging

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QDateTime
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget, QDialog
from PyQt5.QtGui import QImage, QPixmap

# from gui.main_window import Ui_MainWindow
from configs.config import email_address
from gui.main_window_enhanced import Ui_MainWindow
from gui.send_email_report_dialog import Ui_sendEmailDialog
from gui.statistics_widget import Ui_StatisticsWindow
from detect import detect_main, change_vis_stream
from handler.database import MySql
from handler.send_email import Email
from video_stream.visualize import draw_bar_graph, array_to_QImage


# os.environ['CUDA_LAUNCH_BLOCKING'] = "1"  # close PyTorch asynchronous operation


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, detection_flag):
        super().__init__()
        self.detection_flag = detection_flag
        self.setupUi(self)
        self.showFullScreen()
        self.textBrowser.append(time.strftime('%Y-%m-%d %H:%M:%S ',
                                              time.localtime()) + '启动检测...')
        self.statusbar.showMessage('系统初始化...')

        th = DetectionThread(self)
        th.video_1_change_pixmap.connect(self.set_frame_1)
        th.video_2_change_pixmap.connect(self.set_frame_2)
        th.video_3_change_pixmap.connect(self.set_frame_3)
        th.video_4_change_pixmap.connect(self.set_frame_4)
        th.video_5_change_pixmap.connect(self.set_frame_5)
        th.record_change_pixmap.connect(self.set_record)
        th.text_append.connect(self.append_text)
        th.status_update.connect(self.update_status_message)
        th.popup_message_box.connect(self.message_box)
        th.start()
        # print(self.videoLabel.size())
        # print(self.recordLabel.size())

        self.stream_1.triggered.connect(self.switch_vis_stream_1)
        self.stream_2.triggered.connect(self.switch_vis_stream_2)
        self.stream_3.triggered.connect(self.switch_vis_stream_3)
        self.stream_4.triggered.connect(self.switch_vis_stream_4)
        self.stream_5.triggered.connect(self.switch_vis_stream_5)
        self.stop.triggered.connect(self.process_exit)
        self.fullScreen.triggered.connect(self.showFullScreen)
        self.exitFullScreen.triggered.connect(self.showNormal)
        self.setupMenu.triggered.connect(lambda: os.system("notepad configs/config.py"))
        self.openStatistics.triggered.connect(self.open_statistics_window)

        self.pushButton_1.clicked.connect(self.switch_vis_stream_1)
        self.pushButton_2.clicked.connect(self.switch_vis_stream_2)
        self.pushButton_3.clicked.connect(self.switch_vis_stream_3)
        self.pushButton_4.clicked.connect(self.switch_vis_stream_4)
        self.pushButton_5.clicked.connect(self.switch_vis_stream_5)

        self.message_box = None

        self.statistics_window = None

    @pyqtSlot(bool)
    def open_statistics_window(self, trigger):
        self.statistics_window = StatisticsWindow()
        self.statistics_window.show()
        self.statistics_window.pushButton.click()

    @pyqtSlot(QImage)
    def set_frame_1(self, image):
        self.videoLabel_1.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def set_frame_2(self, image):
        self.videoLabel_2.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def set_frame_3(self, image):
        self.videoLabel_3.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def set_frame_4(self, image):
        self.videoLabel_4.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def set_frame_5(self, image):
        self.videoLabel_5.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def set_record(self, image):
        self.recordLabel.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(str)
    def append_text(self, text):
        self.textBrowser.append(text)

    @pyqtSlot(bool)
    def switch_vis_stream_1(self, trigger):
        change_vis_stream(0)

    @pyqtSlot(bool)
    def switch_vis_stream_2(self, trigger):
        change_vis_stream(1)

    @pyqtSlot(bool)
    def switch_vis_stream_3(self, trigger):
        change_vis_stream(2)

    @pyqtSlot(bool)
    def switch_vis_stream_4(self, trigger):
        change_vis_stream(3)

    @pyqtSlot(bool)
    def switch_vis_stream_5(self, trigger):
        change_vis_stream(4)

    @pyqtSlot(str)
    def update_status_message(self, text):
        self.statusbar.showMessage(text)

    @pyqtSlot(bool)
    def process_exit(self, trigger):
        sys.exit()

    @pyqtSlot(str)
    def message_box(self, text):
        if self.message_box is None:
            print("弹窗提示")
            self.message_box = QMessageBox()
            win_x, win_y, win_w, win_h = self.geometry().getRect()  # (x, y, w, h)

            self.message_box.setGeometry((win_x + win_w / 2 - 100), (win_y + win_h / 2 - 100), 0, 0)
            self.message_box.setStyleSheet('''color: rgb(255, 0, 0);
                                         font: 15pt \"黑体\";''')
            self.message_box.critical(self.message_box, "系统异常提示", text)  # 该线程始终在此等待对话框 OK按钮 被点击
            self.message_box = None


class DetectionThread(QThread):
    video_1_change_pixmap = pyqtSignal(QImage)
    video_2_change_pixmap = pyqtSignal(QImage)
    video_3_change_pixmap = pyqtSignal(QImage)
    video_4_change_pixmap = pyqtSignal(QImage)
    video_5_change_pixmap = pyqtSignal(QImage)

    record_change_pixmap = pyqtSignal(QImage)

    text_append = pyqtSignal(str)
    status_update = pyqtSignal(str)

    popup_message_box = pyqtSignal(str)

    def __init__(self, main_window):
        super().__init__(main_window)
        self.detection_flag = main_window.detection_flag
        self.main_window = main_window

    def run(self):
        logging.info('开始检测')
        detect_main(self)


class StatisticsWindow(QMainWindow, Ui_StatisticsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.stop.triggered.connect(self.process_exit)
        self.fullScreen.triggered.connect(self.showFullScreen)
        self.exitFullScreen.triggered.connect(self.showNormal)
        self.pushButton.clicked.connect(self.select_records)
        self.sendEmailRecord.triggered.connect(self.open_send_email_dialog)

        self.startDateTime.setDateTime(QDateTime.currentDateTime().addDays(-1))
        self.endDateTime.setDateTime(QDateTime.currentDateTime())
        self.timeIntervalComboBox.setCurrentIndex(0)
        self.productionLineComboBox.setCurrentIndex(0)

        self.send_email_records_dialog = None

        self.time_interval_combobox_index_dict = {
            0: datetime.timedelta(hours=1),
            1: datetime.timedelta(hours=12),
            2: datetime.timedelta(days=1),
            3: datetime.timedelta(weeks=1),
            4: datetime.timedelta(days=15),
            5: datetime.timedelta(days=30)

        }
        self.graph_names = []
        self.record_numbers = []

    @pyqtSlot(bool)
    def process_exit(self, trigger):
        sys.exit()

    @pyqtSlot(bool)
    def select_records(self, trigger):
        start_datetime = self.startDateTime.dateTime().toPyDateTime()
        end_datetime = self.endDateTime.dateTime().toPyDateTime()
        index = self.timeIntervalComboBox.currentIndex()
        time_interval = self.time_interval_combobox_index_dict[index]

        datetime_periods = []
        temp_datetime = start_datetime + time_interval
        while temp_datetime < end_datetime:
            datetime_periods.append([start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                     temp_datetime.strftime("%Y-%m-%d %H:%M:%S")])
            start_datetime = temp_datetime
            temp_datetime += time_interval
        if temp_datetime != end_datetime or len(datetime_periods) == 0:
            start_datetime = temp_datetime - time_interval
            datetime_periods.append([start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                                     end_datetime.strftime("%Y-%m-%d %H:%M:%S")])

        # print(len(datetime_periods), datetime_periods)
        production_line = self.productionLineComboBox.currentText()
        record_numbers = MySql.count_records_multi_datetime_periods(production_line, datetime_periods)
        # print(len(count_records), count_records)
        if index < 1:
            names = [x[1].split(' ')[1] for x in datetime_periods]
        else:
            names = [x[1].split(' ')[0] for x in datetime_periods]
        # print(names)
        self.graph_names = names
        self.record_numbers = record_numbers
        img = draw_bar_graph(names, record_numbers, production_line + "线 异常事件情况")
        qimg = array_to_QImage(img, self.graphLabel.size())
        self.graphLabel.setPixmap(QPixmap.fromImage(qimg))

    @pyqtSlot(bool)
    def open_send_email_dialog(self, triggered):
        self.send_email_records_dialog = SendEmailDialog(self)
        self.send_email_records_dialog.show()


class SendEmailDialog(QDialog, Ui_sendEmailDialog):
    def __init__(self, statistic_window):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("发送邮件报告")
        self.statistic_window = statistic_window
        self.email_subject, self.email_content = self.get_email_subject_content()

        self.textEdit.append(self.email_subject)
        self.textEdit.append(self.email_content)
        self.lineEdit.setText(email_address)

        self.buttonBox.accepted.connect(self.button_box_accepted)

    @pyqtSlot()
    def button_box_accepted(self):
        success = self.send_email_records(self.email_subject, self.textEdit.toPlainText(), self.lineEdit.text())
        msg_box = QMessageBox()
        msg_box.setWindowTitle("邮件发送反馈")
        if success:
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("报告邮件发送成功^_^ ")
        else:
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("网络出现异常，请稍后重试！")
        msg_box.show()
        msg_box.exec()

    def get_email_subject_content(self) -> (str, str):
        start_datetime = self.statistic_window.startDateTime.dateTime().toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")
        end_datetime = self.statistic_window.endDateTime.dateTime().toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")
        production_line = self.statistic_window.productionLineComboBox.currentText()
        subject = "异常行为事件报告 " + production_line + "工位 " + start_datetime + "至" + end_datetime
        content = ""
        for name, count in zip(self.statistic_window.graph_names, self.statistic_window.record_numbers):
            content += str(name) + "：" + str(count) + "\n"
        return subject, content

    @staticmethod
    def send_email_records(subject: str, content: str, to_account: str) -> bool:
        try:
            Email.send_email(subject, content, from_account="layhal@163.com", SMTP_host="smtp.163.com",
                             from_password="liu670", to_account=to_account)
            print("邮件报告发送成功")
            return True
        except smtplib.SMTPException or Exception as e:
            print("网络出现异常，请稍后重试！", e)
            return False


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def gui_main(detection_flag):
    sys.excepthook = except_hook  # print the traceback to stdout/stderr

    strftime = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime())
    logging.basicConfig(filename='logs/' + strftime + '.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    logging.info('启动检测程序')

    app = QApplication(sys.argv)
    win = MainWindow(detection_flag)
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    import multiprocessing

    flag = multiprocessing.Value('i', 0)
    gui_main(flag)

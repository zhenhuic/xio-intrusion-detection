import os
import sys
import time
import datetime
import logging

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QDateTime
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget
from PyQt5.QtGui import QImage, QPixmap

# from gui.main_window import Ui_MainWindow
from gui.main_window_enhanced import Ui_MainWindow
from gui.statistics_widget import Ui_StatisticsWindow
from detect import detect_main, change_vis_stream
from handler.database import MySql
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

        self.startDateTime.setDateTime(QDateTime.currentDateTime().addDays(-1))
        self.endDateTime.setDateTime(QDateTime.currentDateTime())
        self.timeIntervalComboBox.setCurrentIndex(0)
        self.productionLineComboBox.setCurrentIndex(0)
        self.time_interval_combobox_index_dict = {
            0: datetime.timedelta(hours=1),
            1: datetime.timedelta(hours=12),
            2: datetime.timedelta(days=1),
            3: datetime.timedelta(weeks=1),
            4: datetime.timedelta(days=15),
            5: datetime.timedelta(days=30)

        }

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
        count_records = MySql.count_records_multi_datetime_periods(production_line, datetime_periods)
        # print(len(count_records), count_records)
        if index <= 1:
            names = [x[1].split(' ')[1] for x in datetime_periods]
        else:
            names = [x[1].split(' ')[0] for x in datetime_periods]
        # print(names)
        img = draw_bar_graph(names, count_records)
        qimg = array_to_QImage(img, self.graphLabel.size())
        self.graphLabel.setPixmap(QPixmap.fromImage(qimg))


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

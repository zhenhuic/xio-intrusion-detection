import os
import sys
import time
import logging

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QImage, QPixmap

# from utils.main_window import Ui_MainWindow
from utils.main_window import Ui_MainWindow
from detect import detect_main, change_vis_stream

os.environ['CUDA_LAUNCH_BLOCKING'] = "1"  # close PyTorch asynchronous operation


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textBrowser.append(time.strftime('%Y-%m-%d %H:%M:%S ',
                                              time.localtime()) + '启动检测...')
        self.statusbar.showMessage('系统初始化...')

        dth = DetectionThread(self)
        dth.video_1_change_pixmap.connect(self.set_frame_1)
        dth.video_2_change_pixmap.connect(self.set_frame_2)
        dth.video_3_change_pixmap.connect(self.set_frame_3)
        dth.video_4_change_pixmap.connect(self.set_frame_4)
        dth.video_5_change_pixmap.connect(self.set_frame_5)
        dth.record_change_pixmap.connect(self.set_record)
        dth.text_append.connect(self.append_text)
        dth.status_update.connect(self.update_status_message)
        dth.start()

        # print(self.videoLabel.size())
        # print(self.recordLabel.size())

        self.stream_1.triggered.connect(self.switch_vis_stream_1)
        self.stream_2.triggered.connect(self.switch_vis_stream_2)
        self.stream_3.triggered.connect(self.switch_vis_stream_3)
        self.stream_4.triggered.connect(self.switch_vis_stream_4)
        self.stream_5.triggered.connect(self.switch_vis_stream_5)
        self.stop.triggered.connect(self.process_exit)

        self.pushButton_1.clicked.connect(self.switch_vis_stream_1)
        self.pushButton_2.clicked.connect(self.switch_vis_stream_2)
        self.pushButton_3.clicked.connect(self.switch_vis_stream_3)
        self.pushButton_4.clicked.connect(self.switch_vis_stream_4)
        self.pushButton_5.clicked.connect(self.switch_vis_stream_5)

    @pyqtSlot(QImage)
    def set_frame_1(self, image):
        self.videoLabel_1.setPixmap(QPixmap.fromImage(image))
        self.statusbar.showMessage('正在检测' + ' ' * 110 +
                                   '生产线：萨瓦尼尼-1，萨瓦尼尼-2，专机下线，喷粉上线，薄板通用线')

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


class DetectionThread(QThread):
    video_1_change_pixmap = pyqtSignal(QImage)
    video_2_change_pixmap = pyqtSignal(QImage)
    video_3_change_pixmap = pyqtSignal(QImage)
    video_4_change_pixmap = pyqtSignal(QImage)
    video_5_change_pixmap = pyqtSignal(QImage)

    record_change_pixmap = pyqtSignal(QImage)

    text_append = pyqtSignal(str)
    status_update = pyqtSignal(str)

    def run(self):
        logging.info('开始检测')
        detect_main(self)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    sys.excepthook = except_hook  # print the traceback to stdout/stderr

    strftime = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime())
    logging.basicConfig(filename='logs/' + strftime + '.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    logging.info('启动检测程序')

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

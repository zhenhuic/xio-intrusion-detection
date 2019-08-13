import sys
import time
import logging

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QImage, QPixmap

from utils.main_window import Ui_MainWindow
from detect import detect_main, change_vis_stream


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textBrowser.append(time.strftime('%Y-%m-%d %H:%M:%S ',
                                              time.localtime()) + '启动检测...')
        self.statusbar.showMessage('准备就绪')

        th = Thread(self)
        th.video_change_pixmap.connect(self.set_frame)
        th.record_change_pixmap.connect(self.set_record)
        th.text_append.connect(self.append_text)
        th.start()
        # print(self.videoLabel.size())
        # print(self.recordLabel.size())

        self.stream_1.triggered.connect(self.switch_vis_stream_1)
        self.stream_2.triggered.connect(self.switch_vis_stream_2)
        self.stream_3.triggered.connect(self.switch_vis_stream_3)
        self.stop.triggered.connect(self.process_exit)

    @pyqtSlot(QImage)
    def set_frame(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))
        self.statusbar.showMessage('正在检测' + ' ' * 120 + '生产线：houban, xiazhewan, shangpenfen')

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
    def process_exit(self, trigger):
        sys.exit()


class Thread(QThread):
    video_change_pixmap = pyqtSignal(QImage)
    record_change_pixmap = pyqtSignal(QImage)
    text_append = pyqtSignal(str)

    def run(self):
        logging.info('开始检测')
        detect_main(self)


def main():
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

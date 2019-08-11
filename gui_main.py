import sys

import cv2
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QImage, QPixmap

from main_window import Ui_MainWindow
from detect import detect_main


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        th = Thread(self)
        th.video_change_pixmap.connect(self.set_frame)
        th.start()
        print(self.videoLabel.size())

    @pyqtSlot(QImage)
    def set_frame(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def set_image(self, image):
        self.recordLabel.setPixmap(QPixmap.fromImage(image))


class Thread(QThread):
    video_change_pixmap = pyqtSignal(QImage)
    record_change_pixmap = pyqtSignal(QImage)

    def run(self):
        detect_main(self)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

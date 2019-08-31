# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        MainWindow.setStyleSheet("background-color: rgb(12, 12, 12);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget.setObjectName("centralwidget")
        self.titlelabel = QtWidgets.QLabel(self.centralwidget)
        self.titlelabel.setGeometry(QtCore.QRect(0, 0, 1280, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titlelabel.sizePolicy().hasHeightForWidth())
        self.titlelabel.setSizePolicy(sizePolicy)
        self.titlelabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.titlelabel.setStyleSheet("background-color: rgb(35, 35, 35);\n"
"color: rgb(220, 220, 220);\n"
"font: 24pt \"宋体\";")
        self.titlelabel.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.titlelabel.setObjectName("titlelabel")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 40, 1281, 641))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_1 = QtWidgets.QFrame(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_1.sizePolicy().hasHeightForWidth())
        self.frame_1.setSizePolicy(sizePolicy)
        self.frame_1.setMaximumSize(QtCore.QSize(855, 600))
        self.frame_1.setStyleSheet("background-color: rgb(25, 25, 25);")
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.videoLabel = QtWidgets.QLabel(self.frame_1)
        self.videoLabel.setGeometry(QtCore.QRect(38, 0, 780, 430))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoLabel.sizePolicy().hasHeightForWidth())
        self.videoLabel.setSizePolicy(sizePolicy)
        self.videoLabel.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.videoLabel.setText("")
        self.videoLabel.setObjectName("videoLabel")
        self.infoLabel = QtWidgets.QLabel(self.frame_1)
        self.infoLabel.setGeometry(QtCore.QRect(93, 430, 670, 170))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoLabel.sizePolicy().hasHeightForWidth())
        self.infoLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.infoLabel.setFont(font)
        self.infoLabel.setObjectName("infoLabel")
        self.horizontalLayout.addWidget(self.frame_1)
        self.frame_2 = QtWidgets.QFrame(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMaximumSize(QtCore.QSize(370, 600))
        self.frame_2.setStyleSheet("background-color: rgb(25, 25, 25);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.logTitle = QtWidgets.QLabel(self.frame_2)
        self.logTitle.setGeometry(QtCore.QRect(0, 0, 375, 45))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logTitle.sizePolicy().hasHeightForWidth())
        self.logTitle.setSizePolicy(sizePolicy)
        self.logTitle.setStyleSheet("background-color: rgb(35, 35, 35);\n"
"font: 18pt \"宋体\";\n"
"color: rgb(200, 200, 200);")
        self.logTitle.setObjectName("logTitle")
        self.recordTitle = QtWidgets.QLabel(self.frame_2)
        self.recordTitle.setGeometry(QtCore.QRect(0, 300, 375, 45))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.recordTitle.sizePolicy().hasHeightForWidth())
        self.recordTitle.setSizePolicy(sizePolicy)
        self.recordTitle.setStyleSheet("background-color: rgb(35, 35, 35);\n"
"font: 18pt \"宋体\";\n"
"color: rgb(200, 200, 200);")
        self.recordTitle.setObjectName("recordTitle")
        self.recordLabel = QtWidgets.QLabel(self.frame_2)
        self.recordLabel.setGeometry(QtCore.QRect(6, 351, 358, 243))
        self.recordLabel.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.recordLabel.setText("")
        self.recordLabel.setObjectName("recordLabel")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame_2)
        self.textBrowser.setGeometry(QtCore.QRect(0, 45, 370, 255))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.textBrowser.setFont(font)
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setStyleSheet("gridline-color: rgb(25, 25, 25);\n"
"background-color: rgb(25, 25, 25);\n"
"border-color: rgb(25, 25, 25);\n"
"color: rgb(200, 200, 200);")
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.frame_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 23))
        self.menubar.setStyleSheet("background-color: rgb(35, 35, 35);\n"
"selection-background-color: rgb(100, 100, 100);\n"
"color: rgb(255, 255, 255);")
        self.menubar.setObjectName("menubar")
        self.streammenu = QtWidgets.QMenu(self.menubar)
        self.streammenu.setObjectName("streammenu")
        self.programmenu = QtWidgets.QMenu(self.menubar)
        self.programmenu.setObjectName("programmenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet("background-color: rgb(30, 30, 30);\n"
"color: rgb(255, 255, 255);")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.stream_1 = QtWidgets.QAction(MainWindow)
        self.stream_1.setObjectName("stream_1")
        self.stream_2 = QtWidgets.QAction(MainWindow)
        self.stream_2.setObjectName("stream_2")
        self.stream_3 = QtWidgets.QAction(MainWindow)
        self.stream_3.setObjectName("stream_3")
        self.start = QtWidgets.QAction(MainWindow)
        self.start.setObjectName("start")
        self.stop = QtWidgets.QAction(MainWindow)
        self.stop.setObjectName("stop")
        self.stream_4 = QtWidgets.QAction(MainWindow)
        self.stream_4.setObjectName("stream_4")
        self.stream_5 = QtWidgets.QAction(MainWindow)
        self.stream_5.setObjectName("stream_5")
        self.streammenu.addAction(self.stream_1)
        self.streammenu.addAction(self.stream_2)
        self.streammenu.addAction(self.stream_3)
        self.streammenu.addAction(self.stream_4)
        self.streammenu.addAction(self.stream_5)
        self.programmenu.addAction(self.start)
        self.programmenu.addAction(self.stop)
        self.menubar.addAction(self.programmenu.menuAction())
        self.menubar.addAction(self.streammenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.titlelabel.setText(_translate("MainWindow", "西奥电梯智能安全检测系统"))
        self.infoLabel.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; font-weight:600; color:#c8c8c8;\">系统价值</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7pt;\"> </span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:16pt; color:#c8c8c8;\">1.在线监控设备运行状态,统计设备运行效率；</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:16pt; color:#c8c8c8;\">2.实时捕捉人员状态,对人、机、料进行识别保护；</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:16pt; color:#c8c8c8;\">3.远程对现场人员管理,避免频繁的现场监管检查,节约管理成本；</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:16pt; color:#c8c8c8;\">4.能够自我检查与修复,当系统失效时及时报警提醒,确保生产安全！</span></p></body></html>"))
        self.logTitle.setText(_translate("MainWindow", " 实时检测信息"))
        self.recordTitle.setText(_translate("MainWindow", " 异常记录"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'宋体\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.streammenu.setTitle(_translate("MainWindow", "视频流"))
        self.programmenu.setTitle(_translate("MainWindow", "程序"))
        self.stream_1.setText(_translate("MainWindow", "萨瓦尼尼-1"))
        self.stream_2.setText(_translate("MainWindow", "萨瓦尼尼-2"))
        self.stream_3.setText(_translate("MainWindow", "专机下线"))
        self.start.setText(_translate("MainWindow", "运行"))
        self.stop.setText(_translate("MainWindow", "终止"))
        self.stream_4.setText(_translate("MainWindow", "喷粉上线"))
        self.stream_5.setText(_translate("MainWindow", "薄板通用线"))

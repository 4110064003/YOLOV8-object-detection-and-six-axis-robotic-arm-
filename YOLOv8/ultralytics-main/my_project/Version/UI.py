# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QT.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(979, 726)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ObjectListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.ObjectListWidget.setGeometry(QtCore.QRect(250, 480, 256, 192))
        font = QtGui.QFont()
        font.setFamily("芫荽")
        font.setPointSize(12)
        self.ObjectListWidget.setFont(font)
        self.ObjectListWidget.setObjectName("ObjectListWidget")
        self.TargetListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.TargetListWidget.setGeometry(QtCore.QRect(520, 480, 256, 192))
        font = QtGui.QFont()
        font.setFamily("芫荽")
        font.setPointSize(12)
        self.TargetListWidget.setFont(font)
        self.TargetListWidget.setObjectName("TargetListWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(300, 450, 161, 21))
        font = QtGui.QFont()
        font.setFamily("芫荽")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(570, 450, 161, 21))
        font = QtGui.QFont()
        font.setFamily("芫荽")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.confirmButton = QtWidgets.QPushButton(self.centralwidget)
        self.confirmButton.setGeometry(QtCore.QRect(90, 540, 121, 31))
        font = QtGui.QFont()
        font.setFamily("芫荽")
        font.setPointSize(14)
        self.confirmButton.setFont(font)
        self.confirmButton.setObjectName("confirmButton")
        self.videoLabel = QtWidgets.QLabel(self.centralwidget)
        self.videoLabel.setGeometry(QtCore.QRect(10, 60, 471, 341))
        self.videoLabel.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.videoLabel.setText("")
        self.videoLabel.setObjectName("videoLabel")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(500, 60, 461, 341))
        self.imageLabel.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.imageLabel.setText("")
        self.imageLabel.setObjectName("imageLabel")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(140, 10, 201, 41))
        font = QtGui.QFont()
        font.setFamily("芫荽")
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(570, 10, 341, 41))
        font = QtGui.QFont()
        font.setFamily("芫荽")
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(90, 480, 121, 31))
        font = QtGui.QFont()
        font.setFamily("芫荽")
        font.setPointSize(14)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setGeometry(QtCore.QRect(90, 600, 121, 31))
        font = QtGui.QFont()
        font.setFamily("芫荽")
        font.setPointSize(14)
        self.closeButton.setFont(font)
        self.closeButton.setObjectName("closeButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 979, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "可選擇的夾取物件列表"))
        self.label_2.setText(_translate("MainWindow", "可選擇的放置位置列表"))
        self.confirmButton.setText(_translate("MainWindow", "送出選項"))
        self.label_3.setText(_translate("MainWindow", "操作平台畫面"))
        self.label_4.setText(_translate("MainWindow", "物件偵測以及辨識結果"))
        self.startButton.setText(_translate("MainWindow", "畫面截圖"))
        self.closeButton.setText(_translate("MainWindow", "關閉畫面"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

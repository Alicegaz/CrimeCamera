# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(1306, 841)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 661, 791))
        self.groupBox.setObjectName("groupBox")
        self.stopBtn = QtWidgets.QPushButton(self.groupBox)
        self.stopBtn.setGeometry(QtCore.QRect(170, 520, 71, 41))
        self.stopBtn.setObjectName("stopBtn")
        self.graphicsView = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView.setGeometry(QtCore.QRect(10, 30, 644, 484))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.pauseBtn = QtWidgets.QPushButton(self.groupBox)
        self.pauseBtn.setGeometry(QtCore.QRect(90, 520, 71, 41))
        self.pauseBtn.setObjectName("pauseBtn")
        self.playBtn = QtWidgets.QPushButton(self.groupBox)
        self.playBtn.setGeometry(QtCore.QRect(10, 520, 71, 41))
        self.playBtn.setObjectName("playBtn")
        self.speedUp2 = QtWidgets.QPushButton(self.groupBox)
        self.speedUp2.setGeometry(QtCore.QRect(540, 520, 51, 41))
        self.speedUp2.setObjectName("speedUp2")
        self.speedUp4 = QtWidgets.QPushButton(self.groupBox)
        self.speedUp4.setGeometry(QtCore.QRect(600, 520, 51, 41))
        self.speedUp4.setObjectName("speedUp4")
        self.slowDown4 = QtWidgets.QPushButton(self.groupBox)
        self.slowDown4.setGeometry(QtCore.QRect(360, 520, 51, 41))
        self.slowDown4.setObjectName("slowDown4")
        self.slowDown2 = QtWidgets.QPushButton(self.groupBox)
        self.slowDown2.setGeometry(QtCore.QRect(420, 520, 51, 41))
        self.slowDown2.setObjectName("slowDown2")
        self.speedUp1 = QtWidgets.QPushButton(self.groupBox)
        self.speedUp1.setGeometry(QtCore.QRect(480, 520, 51, 41))
        self.speedUp1.setObjectName("speedUp1")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(680, 10, 611, 791))
        self.groupBox_2.setObjectName("groupBox_2")
        self.facePoolsScrollArea = QtWidgets.QScrollArea(self.groupBox_2)
        self.facePoolsScrollArea.setGeometry(QtCore.QRect(10, 30, 591, 751))
        self.facePoolsScrollArea.setWidgetResizable(True)
        self.facePoolsScrollArea.setObjectName("facePoolsScrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 589, 749))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.facePoolsScrollArea.setWidget(self.scrollAreaWidgetContents_2)
        TabWidget.addTab(self.tab, "")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        TabWidget.addTab(self.tab1, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget"))
        self.groupBox.setTitle(_translate("TabWidget", "Camera view"))
        self.stopBtn.setText(_translate("TabWidget", "Stop"))
        self.pauseBtn.setText(_translate("TabWidget", "Pause"))
        self.playBtn.setText(_translate("TabWidget", "Play"))
        self.speedUp2.setText(_translate("TabWidget", "2x"))
        self.speedUp4.setText(_translate("TabWidget", "4x"))
        self.slowDown4.setText(_translate("TabWidget", "0.25x"))
        self.slowDown2.setText(_translate("TabWidget", "0.5x"))
        self.speedUp1.setText(_translate("TabWidget", "1x"))
        self.groupBox_2.setTitle(_translate("TabWidget", "Faces pool"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "Single Video"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab1), _translate("TabWidget", "Face Search"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TabWidget = QtWidgets.QTabWidget()
    ui = Ui_TabWidget()
    ui.setupUi(TabWidget)
    from slots import SlotsHandler
    from system import System

    system = System()
    slots_handler = SlotsHandler(ui, system)
    TabWidget.show()
    sys.exit(app.exec_())


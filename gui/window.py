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
        TabWidget.resize(1306, 745)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 661, 681))
        self.groupBox.setObjectName("groupBox")
        self.stopBtn = QtWidgets.QPushButton(self.groupBox)
        self.stopBtn.setGeometry(QtCore.QRect(370, 520, 71, 41))
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
        self.pauseBtn.setGeometry(QtCore.QRect(290, 520, 71, 41))
        self.pauseBtn.setObjectName("pauseBtn")
        self.playBtn = QtWidgets.QPushButton(self.groupBox)
        self.playBtn.setGeometry(QtCore.QRect(210, 520, 71, 41))
        self.playBtn.setObjectName("playBtn")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(680, 10, 611, 681))
        self.groupBox_2.setObjectName("groupBox_2")
        self.facePoolsScrollArea = QtWidgets.QScrollArea(self.groupBox_2)
        self.facePoolsScrollArea.setGeometry(QtCore.QRect(10, 40, 591, 631))
        self.facePoolsScrollArea.setWidgetResizable(True)
        self.facePoolsScrollArea.setObjectName("facePoolsScrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 589, 629))
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


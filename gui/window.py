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
        TabWidget.resize(1276, 814)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.graphicsView = QtWidgets.QGraphicsView(self.tab)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 644, 484))
        self.graphicsView.setObjectName("graphicsView")
        self.playBtn = QtWidgets.QPushButton(self.tab)
        self.playBtn.setGeometry(QtCore.QRect(210, 500, 71, 41))
        self.playBtn.setObjectName("playBtn")
        self.pauseBtn = QtWidgets.QPushButton(self.tab)
        self.pauseBtn.setGeometry(QtCore.QRect(290, 500, 71, 41))
        self.pauseBtn.setObjectName("pauseBtn")
        self.stopBtn = QtWidgets.QPushButton(self.tab)
        self.stopBtn.setGeometry(QtCore.QRect(370, 500, 71, 41))
        self.stopBtn.setObjectName("stopBtn")
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
        self.playBtn.setText(_translate("TabWidget", "Play"))
        self.pauseBtn.setText(_translate("TabWidget", "Pause"))
        self.stopBtn.setText(_translate("TabWidget", "Stop"))
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


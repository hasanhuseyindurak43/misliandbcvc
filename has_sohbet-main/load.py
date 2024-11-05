# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'load.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(571, 371)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/img/h.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTip("")
        MainWindow.setStatusTip("")
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(1, 0, 42);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"    font: 75 bold 18pt \"Ubuntu\";\n"
"    color: rgb(199, 133, 0);\n"
"}\n"
"")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("#centralwidget{\n"
"    background-color: rgb(1, 0, 42);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 60, 231, 251))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/img/img/h.png"))
        self.label.setObjectName("label")
        self.birframe = QtWidgets.QFrame(self.centralwidget)
        self.birframe.setGeometry(QtCore.QRect(10, 10, 551, 351))
        self.birframe.setStyleSheet("#birframe{\n"
"    background-color: rgb(87, 137, 139, 200);\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.birframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.birframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.birframe.setObjectName("birframe")
        self.ikiframe = QtWidgets.QFrame(self.birframe)
        self.ikiframe.setGeometry(QtCore.QRect(30, 120, 491, 101))
        self.ikiframe.setStyleSheet("#ikiframe{\n"
"    background-color: rgb(255, 255, 255, 140);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.ikiframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ikiframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ikiframe.setObjectName("ikiframe")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.ikiframe)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 451, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.kads = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.kads.setStyleSheet("#kads{\n"
"    color: rgb(0, 0, 0);\n"
"    font: 75 bold 10pt \"Ubuntu\";\n"
"}")
        self.kads.setObjectName("kads")
        self.horizontalLayout.addWidget(self.kads)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.number = QtWidgets.QLCDNumber(self.verticalLayoutWidget)
        self.number.setStyleSheet("#number{\n"
"    background-color: rgb(255, 255, 255, 100);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    color: rgb(0, 0, 0);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.number.setMidLineWidth(0)
        self.number.setProperty("intValue", 0)
        self.number.setObjectName("number")
        self.horizontalLayout_2.addWidget(self.number)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HAS İDDAA"))
        self.kads.setText(_translate("MainWindow", "HAS İDAA\'YA HOŞGELDİNİZ"))
import icon_rc
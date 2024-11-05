# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dashboard.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 632)
        MainWindow.setMinimumSize(QtCore.QSize(810, 632))
        MainWindow.setMaximumSize(QtCore.QSize(810, 632))
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
"    color: rgb(255, 255, 255);\n"
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
        self.label.setGeometry(QtCore.QRect(290, 210, 231, 251))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/img/img/h.png"))
        self.label.setObjectName("label")
        self.birframe = QtWidgets.QFrame(self.centralwidget)
        self.birframe.setGeometry(QtCore.QRect(10, 10, 791, 611))
        self.birframe.setStyleSheet("#birframe{\n"
"    background-color: rgb(87, 137, 139, 200);\n"
"    border: 1px solid white;\n"
"    border-radius: 10px;\n"
"}")
        self.birframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.birframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.birframe.setObjectName("birframe")
        self.ikiframe = QtWidgets.QFrame(self.birframe)
        self.ikiframe.setGeometry(QtCore.QRect(-145, 10, 141, 301))
        self.ikiframe.setStyleSheet("#ikiframe{\n"
"    background-color: rgb(255, 255, 255, 140);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.ikiframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ikiframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ikiframe.setObjectName("ikiframe")
        self.label_2 = QtWidgets.QLabel(self.ikiframe)
        self.label_2.setGeometry(QtCore.QRect(30, 10, 71, 71))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/kullanıcı/img/user_male3-75.png"))
        self.label_2.setObjectName("label_2")
        self.kad = QtWidgets.QLabel(self.ikiframe)
        self.kad.setGeometry(QtCore.QRect(0, 70, 141, 31))
        self.kad.setStyleSheet("#kad{\n"
"    color: rgb(0, 0, 0);\n"
"    font: 75 bold 10pt \"Ubuntu\";\n"
"}")
        self.kad.setText("")
        self.kad.setAlignment(QtCore.Qt.AlignCenter)
        self.kad.setObjectName("kad")
        self.anasayfa = QtWidgets.QPushButton(self.ikiframe)
        self.anasayfa.setGeometry(QtCore.QRect(20, 110, 90, 28))
        self.anasayfa.setStyleSheet("QPushButton#anasayfa{\n"
"    background-color: rgb(54, 145, 171);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    color: rgb(0, 0, 0);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton#anasayfa:hover{\n"
"    background-color: rgb(255, 255, 255);\n"
"    color: rgb(54, 145, 171);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/anasayfa/img/home-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.anasayfa.setIcon(icon1)
        self.anasayfa.setObjectName("anasayfa")
        self.ayarlar = QtWidgets.QPushButton(self.ikiframe)
        self.ayarlar.setGeometry(QtCore.QRect(20, 150, 90, 28))
        self.ayarlar.setStyleSheet("QPushButton#ayarlar\n"
"{\n"
"    background-color: rgb(54, 145, 171);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    color: rgb(0, 0, 0);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton#ayarlar:hover{\n"
"    background-color: rgb(255, 255, 255);\n"
"    color: rgb(54, 145, 171);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/settings/img/settings-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ayarlar.setIcon(icon2)
        self.ayarlar.setObjectName("ayarlar")
        self.gruplar = QtWidgets.QPushButton(self.ikiframe)
        self.gruplar.setGeometry(QtCore.QRect(20, 190, 90, 28))
        self.gruplar.setStyleSheet("QPushButton#gruplar\n"
"{\n"
"    background-color: rgb(54, 145, 171);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    color: rgb(0, 0, 0);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton#gruplar:hover{\n"
"    background-color: rgb(255, 255, 255);\n"
"    color: rgb(54, 145, 171);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/kullanıcı/img/group-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.gruplar.setIcon(icon3)
        self.gruplar.setObjectName("gruplar")
        self.mesajlar = QtWidgets.QPushButton(self.ikiframe)
        self.mesajlar.setGeometry(QtCore.QRect(20, 230, 90, 28))
        self.mesajlar.setStyleSheet("QPushButton#mesajlar\n"
"{\n"
"    background-color: rgb(54, 145, 171);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    color: rgb(0, 0, 0);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton#mesajlar:hover{\n"
"    background-color: rgb(255, 255, 255);\n"
"    color: rgb(54, 145, 171);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/kişiler/img/contacts-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mesajlar.setIcon(icon4)
        self.mesajlar.setObjectName("mesajlar")
        self.ucframe = QtWidgets.QFrame(self.birframe)
        self.ucframe.setGeometry(QtCore.QRect(-145, 320, 141, 281))
        self.ucframe.setStyleSheet("#ucframe\n"
"{\n"
"    font: 25 italic 10pt \"Ubuntu\";\n"
"    background-color: rgb(255, 255, 255, 140);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.ucframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ucframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ucframe.setObjectName("ucframe")
        self.kadname = QtWidgets.QLabel(self.ucframe)
        self.kadname.setGeometry(QtCore.QRect(10, 10, 101, 31))
        self.kadname.setStyleSheet("#kadname{\n"
"    color: rgb(0, 0, 0);\n"
"    font: 25 italic 10pt \"Ubuntu\";\n"
"}")
        self.kadname.setText("")
        self.kadname.setAlignment(QtCore.Qt.AlignCenter)
        self.kadname.setObjectName("kadname")
        self.ekle = QtWidgets.QPushButton(self.ucframe)
        self.ekle.setGeometry(QtCore.QRect(110, 10, 31, 28))
        self.ekle.setStyleSheet("QPushButton#ekle\n"
"{\n"
"    background-color: rgb(54, 145, 171);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    color: rgb(0, 0, 0);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton#ekle:hover{\n"
"    background-color: rgb(255, 255, 255);\n"
"    color: rgb(54, 145, 171);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.ekle.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/sent/img/sent-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ekle.setIcon(icon5)
        self.ekle.setObjectName("ekle")
        self.dortframe_anasayfa = QtWidgets.QFrame(self.birframe)
        self.dortframe_anasayfa.setGeometry(QtCore.QRect(800, 10, 621, 591))
        self.dortframe_anasayfa.setStyleSheet("#dortframe_anasayfa\n"
"{\n"
"    background-color: rgb(255, 255, 255, 140);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.dortframe_anasayfa.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dortframe_anasayfa.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dortframe_anasayfa.setObjectName("dortframe_anasayfa")
        self.kad_2 = QtWidgets.QLabel(self.dortframe_anasayfa)
        self.kad_2.setGeometry(QtCore.QRect(250, 10, 141, 31))
        self.kad_2.setStyleSheet("#kad{\n"
"    color: rgb(0, 0, 0);\n"
"    font: 75 bold 10pt \"Ubuntu\";\n"
"}")
        self.kad_2.setAlignment(QtCore.Qt.AlignCenter)
        self.kad_2.setObjectName("kad_2")
        self.dortframe_ayarlar = QtWidgets.QFrame(self.birframe)
        self.dortframe_ayarlar.setGeometry(QtCore.QRect(800, 10, 621, 591))
        self.dortframe_ayarlar.setStyleSheet("#dortframe_ayarlar\n"
"{\n"
"    background-color: rgb(255, 255, 255, 140);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.dortframe_ayarlar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dortframe_ayarlar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dortframe_ayarlar.setObjectName("dortframe_ayarlar")
        self.kad_4 = QtWidgets.QLabel(self.dortframe_ayarlar)
        self.kad_4.setGeometry(QtCore.QRect(250, 10, 141, 31))
        self.kad_4.setStyleSheet("#kad{\n"
"    color: rgb(0, 0, 0);\n"
"    font: 75 bold 10pt \"Ubuntu\";\n"
"}")
        self.kad_4.setAlignment(QtCore.Qt.AlignCenter)
        self.kad_4.setObjectName("kad_4")
        self.dortframe_gruplar = QtWidgets.QFrame(self.birframe)
        self.dortframe_gruplar.setGeometry(QtCore.QRect(800, 0, 621, 591))
        self.dortframe_gruplar.setStyleSheet("#dortframe_gruplar\n"
"{\n"
"    background-color: rgb(255, 255, 255, 140);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.dortframe_gruplar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dortframe_gruplar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dortframe_gruplar.setObjectName("dortframe_gruplar")
        self.kad_5 = QtWidgets.QLabel(self.dortframe_gruplar)
        self.kad_5.setGeometry(QtCore.QRect(220, 10, 211, 31))
        self.kad_5.setStyleSheet("#kad{\n"
"    color: rgb(0, 0, 0);\n"
"    font: 75 bold 10pt \"Ubuntu\";\n"
"}")
        self.kad_5.setAlignment(QtCore.Qt.AlignCenter)
        self.kad_5.setObjectName("kad_5")
        self.requests_list = QtWidgets.QListWidget(self.dortframe_gruplar)
        self.requests_list.setGeometry(QtCore.QRect(20, 40, 591, 192))
        self.requests_list.setStyleSheet("#requests_list{\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(0, 0, 0, 150);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.requests_list.setObjectName("requests_list")
        self.kad_7 = QtWidgets.QLabel(self.dortframe_gruplar)
        self.kad_7.setGeometry(QtCore.QRect(210, 240, 211, 31))
        self.kad_7.setStyleSheet("#kad{\n"
"    color: rgb(0, 0, 0);\n"
"    font: 75 bold 10pt \"Ubuntu\";\n"
"}")
        self.kad_7.setAlignment(QtCore.Qt.AlignCenter)
        self.kad_7.setObjectName("kad_7")
        self.friend_list = QtWidgets.QListWidget(self.dortframe_gruplar)
        self.friend_list.setGeometry(QtCore.QRect(20, 270, 591, 192))
        self.friend_list.setStyleSheet("#friend_list{\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(0, 0, 0, 150);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.friend_list.setObjectName("friend_list")
        self.dortframe_mesajlar = QtWidgets.QFrame(self.birframe)
        self.dortframe_mesajlar.setGeometry(QtCore.QRect(800, 10, 621, 591))
        self.dortframe_mesajlar.setStyleSheet("#dortframe_mesajlar\n"
"{\n"
"    background-color: rgb(255, 255, 255, 140);\n"
"    border: 1px;\n"
"    border-radius: 10px;\n"
"}")
        self.dortframe_mesajlar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dortframe_mesajlar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dortframe_mesajlar.setObjectName("dortframe_mesajlar")
        self.kad_6 = QtWidgets.QLabel(self.dortframe_mesajlar)
        self.kad_6.setGeometry(QtCore.QRect(250, 10, 141, 31))
        self.kad_6.setStyleSheet("#kad{\n"
"    color: rgb(0, 0, 0);\n"
"    font: 75 bold 10pt \"Ubuntu\";\n"
"}")
        self.kad_6.setAlignment(QtCore.Qt.AlignCenter)
        self.kad_6.setObjectName("kad_6")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HAS SOHBET"))
        self.anasayfa.setText(_translate("MainWindow", "Anasayfa"))
        self.ayarlar.setText(_translate("MainWindow", "Ayarlar"))
        self.gruplar.setText(_translate("MainWindow", "Arkadaşlar"))
        self.mesajlar.setText(_translate("MainWindow", "Mesaj"))
        self.kad_2.setText(_translate("MainWindow", "ANASAYFA"))
        self.kad_4.setText(_translate("MainWindow", "AYARLAR"))
        self.kad_5.setText(_translate("MainWindow", "GELEN ARKADAŞLIK İSTEKLERİ"))
        self.kad_7.setText(_translate("MainWindow", "EKLİ OLAN ARKADAŞLAR"))
        self.kad_6.setText(_translate("MainWindow", "Mesajlar"))
import icon_rc

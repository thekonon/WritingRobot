# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Control.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDial, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTextBrowser,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.dialButton = QDial(self.centralwidget)
        self.dialButton.setObjectName(u"dialButton")
        self.dialButton.setGeometry(QRect(80, 170, 241, 221))
        self.dialButton.setMaximum(990)
        self.dialButton.setOrientation(Qt.Orientation.Horizontal)
        self.logWindow = QTextBrowser(self.centralwidget)
        self.logWindow.setObjectName(u"logWindow")
        self.logWindow.setGeometry(QRect(390, 30, 361, 461))
        self.connectButton = QPushButton(self.centralwidget)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setGeometry(QRect(40, 90, 121, 51))
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(390, 490, 151, 41))
        self.disconnectButton = QPushButton(self.centralwidget)
        self.disconnectButton.setObjectName(u"disconnectButton")
        self.disconnectButton.setGeometry(QRect(210, 90, 121, 51))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Clear log", None))
        self.disconnectButton.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
    # retranslateUi


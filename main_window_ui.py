# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QListWidget,
    QListWidgetItem, QMainWindow, QPlainTextEdit, QPushButton,
    QSizePolicy, QTabWidget, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1220, 756)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1211, 751))
        self.gallery_tab = QWidget()
        self.gallery_tab.setObjectName(u"gallery_tab")
        self.gallery_list = QListWidget(self.gallery_tab)
        self.gallery_list.setObjectName(u"gallery_list")
        self.gallery_list.setGeometry(QRect(0, 0, 891, 721))
        self.tabWidget.addTab(self.gallery_tab, "")
        self.add_games_tab = QWidget()
        self.add_games_tab.setObjectName(u"add_games_tab")
        self.open_games_list = QListWidget(self.add_games_tab)
        self.open_games_list.setObjectName(u"open_games_list")
        self.open_games_list.setGeometry(QRect(0, 40, 521, 661))
        self.add_game_btn = QPushButton(self.add_games_tab)
        self.add_game_btn.setObjectName(u"add_game_btn")
        self.add_game_btn.setGeometry(QRect(540, 50, 121, 41))
        self.remove_game_btn = QPushButton(self.add_games_tab)
        self.remove_game_btn.setObjectName(u"remove_game_btn")
        self.remove_game_btn.setGeometry(QRect(540, 180, 121, 41))
        self.games_to_watch_list = QListWidget(self.add_games_tab)
        self.games_to_watch_list.setObjectName(u"games_to_watch_list")
        self.games_to_watch_list.setGeometry(QRect(680, 40, 521, 661))
        self.open_procs_label = QLabel(self.add_games_tab)
        self.open_procs_label.setObjectName(u"open_procs_label")
        self.open_procs_label.setGeometry(QRect(130, 20, 151, 16))
        self.games_to_watch_label = QLabel(self.add_games_tab)
        self.games_to_watch_label.setObjectName(u"games_to_watch_label")
        self.games_to_watch_label.setGeometry(QRect(890, 20, 151, 16))
        self.tabWidget.addTab(self.add_games_tab, "")
        self.settings_tab = QWidget()
        self.settings_tab.setObjectName(u"settings_tab")
        self.tabWidget.addTab(self.settings_tab, "")
        self.Shrink = QWidget()
        self.Shrink.setObjectName(u"Shrink")
        self.dropFrame = QFrame(self.Shrink)
        self.dropFrame.setObjectName(u"dropFrame")
        self.dropFrame.setGeometry(QRect(10, 10, 651, 701))
        self.dropFrame.setAcceptDrops(True)
        self.dropFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.dropFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.tabWidget.addTab(self.Shrink, "")
        self.logs_tab = QWidget()
        self.logs_tab.setObjectName(u"logs_tab")
        self.logOutput = QPlainTextEdit(self.logs_tab)
        self.logOutput.setObjectName(u"logOutput")
        self.logOutput.setGeometry(QRect(0, 0, 1201, 721))
        self.logOutput.setReadOnly(True)
        self.tabWidget.addTab(self.logs_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.gallery_tab), QCoreApplication.translate("MainWindow", u"Gallery", None))
        self.add_game_btn.setText(QCoreApplication.translate("MainWindow", u"Add Game", None))
        self.remove_game_btn.setText(QCoreApplication.translate("MainWindow", u"Remove Game", None))
        self.open_procs_label.setText(QCoreApplication.translate("MainWindow", u"Open Processes", None))
        self.games_to_watch_label.setText(QCoreApplication.translate("MainWindow", u"Games to watch", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.add_games_tab), QCoreApplication.translate("MainWindow", u"Add Games", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings_tab), QCoreApplication.translate("MainWindow", u"Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Shrink), QCoreApplication.translate("MainWindow", u"Embed", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logs_tab), QCoreApplication.translate("MainWindow", u"Logs", None))
    # retranslateUi


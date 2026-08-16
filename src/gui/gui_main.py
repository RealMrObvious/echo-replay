from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon
from .tray import Tray
from .ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QIcon("media/icon.png"))

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.hide()

        self.tray = Tray(QApplication.instance(), self)

    def open_gallery(self):
        self.open_tab(self.ui.gallery_tab)

    def open_settings(self):
        self.open_tab(self.ui.settings_tab)

    def open_add_games(self):
        self.open_tab(self.ui.add_games_tab)

    def open_logs(self):
        self.open_tab(self.ui.logs_tab)

    def open_tab(self, tab):
        self.ui.tabWidget.setCurrentWidget(tab)
        self.show()

        # Bring the window to the front
        self.raise_()
        self.activateWindow()

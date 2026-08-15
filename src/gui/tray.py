from PyQt6.QtGui import QIcon, QDesktopServices, QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu 
from PyQt6.QtCore import QUrl
from pathlib import Path

class Tray(QSystemTrayIcon):
    def __init__(self, app, parent=None):
        icon = QIcon("media/icon.png")

        super().__init__(icon, parent)

        self.app = app

        self.menu = QMenu()

        self.option1 = QAction("Open App", self.menu)
        self.option2 = QAction("Settings", self.menu)
        self.option2.triggered.connect(self.open_settings)
        self.quit_action = QAction("Exit", self.menu)

        self.menu.addAction(self.option1)
        self.menu.addAction(self.option2)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.quit_action.triggered.connect(app.quit)

        self.setContextMenu(self.menu)
        self.show()

        print("Tray created")

    def open_settings(self):
        settings_path = Path("config.json").resolve()
        QDesktopServices.openUrl(
            QUrl.fromLocalFile(str(settings_path))
        )
from PyQt6.QtGui import QIcon, QDesktopServices, QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu 
from PyQt6.QtCore import QUrl
from pathlib import Path

class Tray(QSystemTrayIcon):
    def __init__(self, app, parent=None):
        icon = QIcon("media/icon.png")

        super().__init__(icon, parent)

        self.app = app
        self.window = parent

        self.menu = QMenu()

        self.open_action = QAction("Open App", self.menu)
        self.add_game_action = QAction("Add Game", self.menu)
        self.settings_action = QAction("Settings", self.menu)
        self.logs_action = QAction("Open Logs", self.menu)
        self.quit_action = QAction("Exit", self.menu)

        self.menu.addAction(self.open_action)
        self.menu.addAction(self.add_game_action)
        self.menu.addAction(self.settings_action)
        self.menu.addAction(self.logs_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.activated.connect(self.window.open_gallery)
        self.open_action.triggered.connect(self.window.open_gallery)
        self.add_game_action.triggered.connect(self.window.open_add_games)
        self.settings_action.triggered.connect(self.window.open_settings)
        self.logs_action.triggered.connect(self.window.open_logs)
        self.quit_action.triggered.connect(app.quit)

        self.setContextMenu(self.menu)
        self.show()
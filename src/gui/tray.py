from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtCore import QObject


class Tray(QSystemTrayIcon):
    def __init__(self, app, parent=None):
        super().__init__(QIcon("media/icon.png"), parent)

        self.app = app
        self.window = parent

        self.menu = QMenu()

        self.open_action = QAction("Open App", self.menu)
        self.add_game_action = QAction("Add Game", self.menu)
        self.share_action = QAction("Share Videos", self.menu)
        self.settings_action = QAction("Settings", self.menu)
        self.logs_action = QAction("Open Logs", self.menu)
        self.quit_action = QAction("Exit", self.menu)

        self.menu.addAction(self.open_action)
        self.menu.addAction(self.add_game_action)
        self.menu.addAction(self.share_action)
        self.menu.addAction(self.settings_action)
        self.menu.addAction(self.logs_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.activated.connect(self.on_activated)

        self.open_action.triggered.connect(self.window.open_gallery)
        self.add_game_action.triggered.connect(self.window.open_add_games)
        self.share_action.triggered.connect(self.window.open_share)
        self.settings_action.triggered.connect(self.window.open_settings)
        self.logs_action.triggered.connect(self.window.open_logs)
        self.quit_action.triggered.connect(self.app.quit)

        # Qt handles right-click automatically
        self.setContextMenu(self.menu)

        self.show()

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.window.open_gallery()

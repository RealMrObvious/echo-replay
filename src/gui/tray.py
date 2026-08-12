from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QMenu 

class Tray(QSystemTrayIcon):
    def __init__(self, app, parent=None):
        icon = QIcon("media/icon.png")

        super().__init__(icon, parent)

        self.app = app

        self.menu = QMenu()

        self.option1 = QAction("Open App", self.menu)
        self.option2 = QAction("Settings", self.menu)
        self.quit_action = QAction("Exit", self.menu)

        self.menu.addAction(self.option1)
        self.menu.addAction(self.option2)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.quit_action.triggered.connect(app.quit)

        self.setContextMenu(self.menu)
        self.show()

        print("Tray created")
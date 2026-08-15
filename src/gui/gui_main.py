from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout
from .tray import Tray

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 400, 300)
        self.hide()

        self.setCentralWidget(CenterPane())

        self.tray = Tray(QApplication.instance(), self)

class CenterPane(QWidget):
    # While this class does not currently contain much what it does 
    # contain is essential and it allows for expansion later on --
    # for example what if instead of a single textbox one wants a
    # tree and a list view that would be handled here
    def __init__(self):
        QWidget.__init__(self)
        hbox = QHBoxLayout(self)
from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import QEvent, QObject, pyqtSignal, pyqtSlot, QPropertyAnimation, QEasingCurve, QMimeData, QUrl, Qt

class SettingsTab(QObject):
    file_selected  = pyqtSignal(str)

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
                
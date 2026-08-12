from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import keyboard


class HotkeyListener(QObject):
    finished = pyqtSignal()
    save_clip_requested = pyqtSignal()

    def __init__(self, hotkey):
        super().__init__()
        self.hotkey = hotkey

    def start(self):
        keyboard.add_hotkey(
            self.hotkey,
            self.on_hotkey
        )

    def on_hotkey(self):
        print("Hotkey pressed")
        self.save_clip_requested.emit()
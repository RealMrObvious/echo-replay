from PyQt5.QtCore import QObject, QThread, pyqtSignal
from process import wait_for_game_open, wait_for_game_close


class GameWatcher(QObject):
    finished = pyqtSignal()
    game_started = pyqtSignal(str, int)
    game_closed = pyqtSignal(str)

    def __init__(self, games):
        super().__init__()
        self.games = games

    def run(self):
        games = self.games
        
        while not QThread.currentThread().isInterruptionRequested():

            # Search for a game from the list to open
            pid, game = wait_for_game_open(
                games,
                QThread.currentThread()
            )

            if QThread.currentThread().isInterruptionRequested():
                break

            if pid is None:
                break

            print(f"Found game: {game}")

            self.game_started.emit(game, pid)

            # Keep this as our main game until it closes
            wait_for_game_close(
                pid,
                game,
                QThread.currentThread()
            )

            if QThread.currentThread().isInterruptionRequested():
                break

            print(f"Game ({game}) Closed")

            self.game_closed.emit(game)

        self.finished.emit()
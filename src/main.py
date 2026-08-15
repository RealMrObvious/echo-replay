from gui.gui_main import MainWindow
from game_watcher import GameWatcher
from hotkey_listener import HotkeyListener
from obs_controller import ObsController
import sys
from config import load_config
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread
import time

def cleanup():
    print()
#     global obs_client

#     shutdown_event.set()

#     SHUTDOWN_EVENT = shutdown_event

#     if obs_client is not None:
#         stop_replay_buffer(
#             host=config["host"],
#             port=config["port"],
#             password=config["password"],
#             timeout=config["obs_timeout"],
#         )

#     stop_obs()


def main():
    global config
    config = load_config()

    obs = ObsController(
        obs_path = config["obs_path"],
        host = config["host"],
        port = config["port"],
        password = config["password"],
        timeout = config["obs_timeout"],
        use_dedicated_scene = config["use_dedicated_scene"],
        dedicated_scene_name = config["dedicated_scene_name"],
        output_directory = config["output_directory"],
    )

    obs.start_obs()

    print("Starting GUI")

    time.sleep(3)

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    GUI = MainWindow()
    GUI.hide()

    game_watcher_thread = QThread()
    hotkey_listener_thread = QThread()
    
    game_watcher = GameWatcher(config['games'])
    game_watcher.moveToThread(game_watcher_thread)
    game_watcher.game_started.connect(obs.on_game_started)
    game_watcher.game_closed.connect(obs.on_game_closed)

    hotkey_listener = HotkeyListener(config['hotkey'])
    hotkey_listener.save_clip_requested.connect(obs.save_clip)

    # game_watcher.moveToThread(game_watcher_thread)
    hotkey_listener.moveToThread(hotkey_listener_thread)

    game_watcher_thread.started.connect(game_watcher.run)
    hotkey_listener_thread.started.connect(hotkey_listener.start)

    game_watcher.finished.connect(game_watcher_thread.quit)
    game_watcher.finished.connect(game_watcher.deleteLater)
    game_watcher_thread.finished.connect(game_watcher_thread.deleteLater)

    hotkey_listener.finished.connect(hotkey_listener_thread.quit)
    hotkey_listener.finished.connect(hotkey_listener.deleteLater)
    hotkey_listener_thread.finished.connect(hotkey_listener_thread.deleteLater)

    game_watcher_thread.start()
    hotkey_listener_thread.start()

    app.aboutToQuit.connect(game_watcher_thread.requestInterruption)
    app.aboutToQuit.connect(hotkey_listener_thread.requestInterruption)
    app.aboutToQuit.connect(obs.stop_obs)

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping...")
        cleanup()
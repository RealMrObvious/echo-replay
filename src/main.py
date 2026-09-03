from gui.gui_main import MainWindow
from game_watcher import GameWatcher
from hotkey_listener import HotkeyListener
from obs_controller import ObsController
from ffmpeg_controller import FFmpegController
from config import load_config
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread
import sys

def main():
    config = load_config()

    #TODO: These need to be set somewhere properly

    config["target_mb"] = 19
    config["selected_codec"] = "av1_amf"
    config["target_h_res"] = 1920
    config["target_v_res"] = 1080
    config["audio_kbps"] = 128

    encoder = FFmpegController(
            target_mb = config["target_mb"], 
            selected_codec = config["selected_codec"],
            target_h_res = config["target_h_res"],
            target_v_res = config["target_v_res"],
            audio_kbps= config["audio_kbps"],
            )

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

    obs.start_or_connect_obs()

    print("Starting GUI")

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    GUI = MainWindow()
    GUI.hide()

    game_watcher_thread = QThread()
    hotkey_listener_thread = QThread()
    encoder_thread = QThread()

    # Game Watcher Thread Stuff
    
    game_watcher = GameWatcher(config['games'])
    game_watcher.moveToThread(game_watcher_thread)

    game_watcher.game_started.connect(obs.on_game_started)
    game_watcher.game_closed.connect(obs.on_game_closed)

    game_watcher.finished.connect(game_watcher_thread.quit)
    game_watcher.finished.connect(game_watcher.deleteLater)

    game_watcher_thread.started.connect(game_watcher.run)
    game_watcher_thread.finished.connect(game_watcher_thread.deleteLater)

    print("Waiting for game to start...")

    # Hotkey Listener Thread Stuff

    hotkey_listener = HotkeyListener(config['hotkey'])
    hotkey_listener.save_clip_requested.connect(obs.save_clip)
    hotkey_listener.moveToThread(hotkey_listener_thread)
   
    hotkey_listener.finished.connect(hotkey_listener_thread.quit)
    hotkey_listener.finished.connect(hotkey_listener.deleteLater)

    hotkey_listener_thread.started.connect(hotkey_listener.start)
    hotkey_listener_thread.finished.connect(hotkey_listener_thread.deleteLater)

    # Encoder Thread Stuff
    
    encoder.moveToThread(encoder_thread)

    GUI.share_tab.file_selected.connect(encoder.files_received)
    encoder.thumbnail_ready.connect(GUI.share_tab.set_thumbnail)
    encoder.progress.connect(GUI.share_tab.update_progress)
    encoder.finished.connect(GUI.share_tab.encoding_finished)
    encoder.error.connect(GUI.share_tab.encoding_error)

    # Start all threads

    game_watcher_thread.start()
    hotkey_listener_thread.start()
    encoder_thread.start()

    app.aboutToQuit.connect(game_watcher_thread.requestInterruption)
    app.aboutToQuit.connect(hotkey_listener_thread.requestInterruption)
    app.aboutToQuit.connect(encoder_thread.requestInterruption)
    app.aboutToQuit.connect(obs.stop_obs)

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping...")
import threading
import keyboard
import pystray
from PIL import Image
from obs_control import stop_obs, stop_replay_buffer
import sys
from helper import resource_path


def quit_app(icon, item, config, shutdown_event):
    """
    Cleanup before exiting.
    """
    stop_replay_buffer(
                host=config["host"],
                port=config["port"],
                password=config["password"],
                timeout=config["obs_timeout"],
            )
    stop_obs()

    shutdown_event.set()

    icon.stop()
    sys.exit(0)


def start_tray(config, shutdown_event):
    image = Image.open(resource_path("media/icon.png"))

    menu = pystray.Menu(
        pystray.MenuItem(
            "Exit",
            lambda icon, item: quit_app(icon, item, config, shutdown_event)
        )
    )

    icon = pystray.Icon(
        "Echo Replay",
        image,
        "Echo Replay",
        menu
    )

    icon.run()


def start_gui(config, clip_callback, shutdown_event):
    """
    Starts:
    - Global hotkeys
    - System tray
    """

    hotkey = config['hotkey']

    keyboard.add_hotkey(
        hotkey,
        clip_callback
    )

    threading.Thread(
        target=start_tray,
        args=(config,shutdown_event,),
        daemon=True
    ).start()
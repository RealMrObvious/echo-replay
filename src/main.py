from gui import start_gui
from config import load_config
from process import check_for_running_games, check_running_game
from playsound3 import playsound
from obs_control import (
    start_replay_buffer,
    start_obs,
    stop_replay_buffer,
    stop_obs,
)

import threading
import time
from pathlib import Path


shutdown_event = threading.Event()
obs_client = None


def get_latest_clip(cl):
    directory = Path(cl.get_record_directory().record_directory)

    clips = [
        f for f in directory.iterdir()
        if f.is_file()
    ]

    if not clips:
        return None

    return max(clips, key=lambda f: f.stat().st_mtime)


def save_clip():
    global obs_client

    if obs_client is None:
        print("OBS not ready")
        return

    print("Saving clip...")
    
    obs_client.save_replay_buffer()
    playsound("media/chime.mp3")

    time.sleep(0.5)

    if(not obs_client):
        print(f"Saved clip")
    else:
        print(f"Saved clip to {get_latest_clip(obs_client)}")


def wait_for_game(games):
    while not shutdown_event.is_set():
        pid, name = check_for_running_games(games)

        if pid:
            return pid, name

        time.sleep(2)

    return None, None


def wait_for_game_close(pid, name):
    while not shutdown_event.is_set():
        pid, name = check_running_game(pid, name)

        if pid is None:
            return

        time.sleep(3)


def watch_games(config):
    global obs_client

    while not shutdown_event.is_set():

        pid, name = wait_for_game(config["games"])

        if shutdown_event.is_set() or pid is None:
            break

        print(f"Found game: {name}")

        obs_client = start_replay_buffer(
            host=config["host"],
            port=config["port"],
            password=config["password"],
            title=name,
            output_directory=config["output_directory"],
            timeout=config["obs_timeout"],
            use_dedicated_scene=config["use_dedicated_scene"],
            dedicated_scene_name=config["dedicated_scene_name"],
        )

        wait_for_game_close(pid, name)

        if shutdown_event.is_set():
            break

        print("Game Closed")

        stop_replay_buffer(
            host=config["host"],
            port=config["port"],
            password=config["password"],
            timeout=config["obs_timeout"],
        )

        obs_client = None


def cleanup():
    global obs_client

    shutdown_event.set()

    if obs_client is not None:
        stop_replay_buffer(
            host=config["host"],
            port=config["port"],
            password=config["password"],
            timeout=config["obs_timeout"],
        )

    stop_obs()


def main():
    global config

    config = load_config()

    start_obs(config["obs_path"])

    print("Starting GUI thread")

    threading.Thread(
        target=start_gui,
        args=(config, save_clip, shutdown_event),
        daemon=True,
    ).start()

    print("Starting watcher thread")

    threading.Thread(
        target=watch_games,
        args=(config,),
        daemon=True,
    ).start()

    print("Threads started")
    print("Echo Replay running")

    try:
        shutdown_event.wait()
    except KeyboardInterrupt:
        print("\nStopping...")
        cleanup()

    print("Exiting...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping...")
        cleanup()
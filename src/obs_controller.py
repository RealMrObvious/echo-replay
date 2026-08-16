import obsws_python as obs
import subprocess
import os, time
from process_watcher import check_for_running_programs, get_process, popen_to_psutil_process
from playsound3 import playsound
from helper import *

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class ObsController(QObject):
    finished = pyqtSignal()
    ready = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(
        self,
        obs_path=None,
        host="localhost",
        port=4455,
        password="mystrongpass",
        timeout=5,
        use_dedicated_scene=True,
        dedicated_scene_name="clips",
        output_directory="",
    ):
        super().__init__()

        self.obs_path = obs_path
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
        self.use_dedicated_scene = use_dedicated_scene
        self.dedicated_scene_name = dedicated_scene_name
        self.output_directory = output_directory

        self.obs_process = None
        self.obs = None
        self.input_name = "Echo Replay - Game Capture"
        self.target_executable = None               # The target executable
        self.target_pid = None
        self.target_window = None                   # OBS custom name for the target executable for game capture
        self.item_id = None                         # ID of an item within a scene (ie. gamecapture -> id=3)
        

    def run(self):
        self.finished.emit()

    def start_or_connect_obs(self):

        obs_list = [
            {'name': 'obs', 'path': 'obs64.exe'}, 
            {'name': 'obs', 'path': 'obs32.exe'},
            ]

        existing_obs_process = None
        obs_pid, ___ = check_for_running_programs(obs_list)
        print(f"OBS PID: {obs_pid}")

        if(obs_pid is not None):
            existing_obs_process = get_process(obs_pid)
            print(f"Found existing OBS process: {existing_obs_process}")

        if(existing_obs_process is None):
            obs_path = self.obs_path
            obs_bin = os.path.dirname(obs_path)

            print(f"Starting new OBS process: {existing_obs_process}")
            
            self.obs_process = subprocess.Popen(
                [
                    obs_path,
                    "--minimize-to-tray",
                    "--disable-shutdown-check" 
                ],
                cwd=obs_bin
            )

            self.obs_process = popen_to_psutil_process(self.obs_process)

        else:
            self.obs_process = existing_obs_process
            print("OBS already running, connecting to WebSocket server...")
    
        # Give OBS time to start up
        time.sleep(self.timeout)
        self.connect_obs()

        # Give OBS time to processing
        time.sleep(self.timeout)

        if(Path(self.output_directory).is_dir() == False):
            raise ValueError(
                f"Output directory does not exist: {self.output_directory}"
            )

        self.set_record_directory()

    def set_record_directory(self):
        directory = self.output_directory

        for attempt in range(1, 10):
            try:
                self.obs.set_record_directory(directory)

                print("OBS is ready.")
                return True

            except obs.error.OBSSDKRequestError as e:
                print(
                    f"OBS not ready "
                    f"(attempt {attempt}/10): {e}"
                )

                time.sleep(1)

        raise Exception("OBS did not become ready, could not set record directory.")

    def stop_obs(self):
        """
        Closes OBS if it was started by the clipper.
        """

        obs_process = self.obs_process
        
        if obs_process is None or not obs_process.is_running():
            return

        self.stop_replay_buffer()
        print("Closing OBS...")
        obs_process.terminate()

        try:
            obs_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Force closing OBS...")
            obs_process.kill()

    def connect_obs(self):
        """
        Creates and returns an OBS WebSocket client.
        """

        for i in range(5):
            try:
                obs_client = obs.ReqClient(
                    host=self.host,
                    port=self.port,
                    password=self.password,
                    timeout=self.timeout
                )

                self.obs = obs_client
                return obs_client

            except Exception as e:
                print(f"Failed attempt {i+1}/5 to connect to OBS WebSocket server: {e}")
                time.sleep(2)

        raise Exception(
            f"Unable to connect to OBS.\n"
            f"Connecting to {self.host}:{self.port}"
        )

    def ensure_scene(self):
        """
        Creates the scene if it does not exist,
        then switches OBS to that scene.
        """

        scenes = self.obs.get_scene_list().scenes

        scene_names = [
            scene["sceneName"]
            for scene in scenes
        ]

        if self.dedicated_scene_name not in scene_names:
            print(f"Creating scene ({self.dedicated_scene_name})...")
            self.obs.create_scene(self.dedicated_scene_name)

        self.obs.set_current_program_scene(self.dedicated_scene_name)

    def get_scene_sources(self):
        """
        Returns all source names inside a scene.
        """

        items = self.obs.get_scene_item_list(
            self.dedicated_scene_name
        ).scene_items

        return [
            item["sourceName"]
            for item in items
        ]

    def create_game_capture(self):
        """
        Creates a Game Capture source.
        """

        print("Creating Game Capture source...")

        self.obs.create_input(
            sceneName=self.dedicated_scene_name,
            inputName=self.input_name,
            inputKind="game_capture",
            inputSettings={
                "capture_mode": "window",
                "capture_method": "WGC"
            },
            sceneItemEnabled=True
        )

    def get_game_window(self):
        """
        Finds the targeted executable from the list of available windows to capture

        OBS needs:
            Title:Class:Executable

        instead of only the window title.
        """

        props = self.obs.get_input_properties_list_property_items(
            input_name=self.input_name,
            prop_name="window"
        )

        for window in props.property_items:

            # print(self.target_executable.lower(), window)

            if self.target_executable.lower() in window["itemName"].lower():
                self.target_window = window["itemValue"]
                break

    def update_game_capture(self):
        """
        Applies the selected window to the capture source.
        """

        self.obs.set_input_settings(
            self.input_name,
            {
                "capture_mode": "window",
                "window": self.target_window,
                "capture_method": "WGC",
                "capture_audio": True
            },
            overlay = True
        )

        self.obs.set_profile_parameter(
            "AdvOut",
            "RecRBTime",
            str(120)
            )

    def get_scene_item_id(self):
        """
        Gets the OBS scene item ID for a source.
        """

        items = self.obs.get_scene_item_list(
            self.dedicated_scene_name
        ).scene_items

        for item in items:
            if item["sourceName"] == self.input_name:
                self.item_id = item["sceneItemId"]

    def fit_source_to_canvas(self):
        """
        Scales the source to fit OBS canvas size.
        """

        video_settings = self.obs.get_video_settings()

        width = video_settings.base_width
        height = video_settings.base_height

        print(f"OBS canvas: {width}x{height}")

        self.obs.set_scene_item_transform(
            scene_name=self.dedicated_scene_name,
            item_id=self.item_id,
            transform={
                "positionX": width / 2,
                "positionY": height / 2,
                "rotation": 0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "alignment": 0,
                "boundsType": "OBS_BOUNDS_SCALE_INNER",
                "boundsAlignment": 0,
                "boundsWidth": width,
                "boundsHeight": height
            }
        )

    def setup_capture_source(self):
        """
        Creates and configures the Game Capture source.
        """

        sources = self.get_scene_sources()

        if self.input_name not in sources:
            self.create_game_capture()

        print("Finding OBS window...")

        # Wait 30 seconds for window to appear.
        for i in range(30):
            self.get_game_window()

            if(self.target_window):
                break

            time.sleep(5)

        if not self.target_window:
            raise Exception(
                f"Unable to find '{self.target_executable}' in OBS window list"
            )

        print(f"Using OBS window: {self.target_window}")

        self.update_game_capture()

    def obs_setup(self):

        self.ensure_scene()
        self.setup_capture_source()
        self.get_scene_item_id()

        if self.item_id is None:
            raise Exception(
                f"Could not find scene item {self.input_name}"
            )

        self.fit_source_to_canvas()

    def start_replay_buffer(self):
        try:
            status = self.obs.get_replay_buffer_status()

            if not status.output_active:
                print("Starting replay buffer...")
                self.obs.start_replay_buffer()
        except Exception as e:
            raise Exception(f"Error getting replay buffer status: {e}. \nHave you enabled the Replay Buffer in OBS settings?")


    def stop_replay_buffer(self):
        status = self.obs.get_replay_buffer_status()

        if status.output_active:
            print("Stopping replay buffer...")
            self.obs.stop_replay_buffer()

    def save_clip(self):
        if self.obs is None:
            print("OBS not ready")
            return

        print("Saving clip...")
        
        self.obs.save_replay_buffer()
        playsound(str(resource_path("media/clip_saved.mp3")))

        time.sleep(0.5)

        clip = self.get_latest_clip()

        print(f"Saved clip to {clip}")


    def get_latest_clip(self):
        directory = Path(self.obs.get_record_directory().record_directory)

        clips = [
            f for f in directory.iterdir()
            if f.is_file()
        ]

        if not clips:
            return None

        return max(clips, key=lambda f: f.stat().st_mtime)


    @pyqtSlot(str, int)
    def on_game_started(self, game, pid):
        print(f"Game started: {game}, PID: {pid}")

        self.target_executable = game
        self.target_pid = pid

        self.obs_setup()
        self.start_replay_buffer()
        playsound(str(resource_path("media/game_on.mp3")))

    @pyqtSlot()
    def on_game_closed(self):
        print(f"Game closed: {self.target_executable}")

        self.target_executable = None
        self.target_pid = None
        self.target_window = None 

        self.stop_replay_buffer()
        playsound(str(resource_path("media/game_off.mp3")))
        
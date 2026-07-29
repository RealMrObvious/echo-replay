import obsws_python as obs
import subprocess
import os, time

obs_process= None

def start_obs(obs_path):
    """
    Starts OBS with the correct working directory.
    """
    global obs_process 

    obs_bin = os.path.dirname(obs_path)

    obs_process = subprocess.Popen(
        [
            obs_path,
            "--minimize-to-tray",
            "--disable-shutdown-check" 
        ],
        cwd=obs_bin
    )

    # Give OBS time to start WebSocket server
    time.sleep(5)

def stop_obs():
    """
    Closes OBS if it was started by the clipper.
    """

    global obs_process

    if obs_process is None:
        return

    if obs_process.poll() is None:
        print("Closing OBS...")
        obs_process.terminate()

        try:
            obs_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Force closing OBS...")
            obs_process.kill()

def connect_obs(host, port, password, timeout):
    """
    Creates and returns an OBS WebSocket client.
    """

    try:
        return obs.ReqClient(
            host=host,
            port=port,
            password=password,
            timeout=timeout
        )

    except Exception:
        raise Exception(
            f"Unable to connect to OBS.\n"
            f"Connecting to {host}:{port}"
        )


def ensure_scene(cl, scene_name):
    """
    Creates the scene if it does not exist,
    then switches OBS to that scene.
    """

    scenes = cl.get_scene_list().scenes

    scene_names = [
        scene["sceneName"]
        for scene in scenes
    ]

    if scene_name not in scene_names:
        print(f"Creating scene ({scene_name})...")
        cl.create_scene(scene_name)

    cl.set_current_program_scene(scene_name)


def get_scene_sources(cl, scene_name):
    """
    Returns all source names inside a scene.
    """

    items = cl.get_scene_item_list(
        scene_name
    ).scene_items

    return [
        item["sourceName"]
        for item in items
    ]


def create_game_capture(cl, scene_name, source_name):
    """
    Creates a Game Capture source.
    """

    print("Creating Game Capture source...")

    cl.create_input(
        sceneName=scene_name,
        inputName=source_name,
        inputKind="game_capture",
        inputSettings={
            "capture_mode": "window",
            "capture_method": "WGC"
        },
        sceneItemEnabled=True
    )


def get_game_window(cl, title):
    """
    Finds the OBS formatted window identifier.

    OBS needs:
        Title:Class:Executable

    instead of only the window title.
    """

    props = cl.get_input_properties_list_property_items(
        input_name="Game Capture",
        prop_name="window"
    )

    for window in props.property_items:

        # print(title.lower(), window)

        if title.lower() in window["itemName"].lower():
            return window["itemValue"]

    return None


def update_game_capture(cl, source_name, window):
    """
    Applies the selected window to the capture source.
    """

    cl.set_input_settings(
        source_name,
        {
            "capture_mode": "window",
            "window": window,
            "capture_method": "WGC"
        },
        True
    )


def get_scene_item_id(cl, scene_name, source_name):
    """
    Gets the OBS scene item ID for a source.
    """

    items = cl.get_scene_item_list(
        scene_name
    ).scene_items

    for item in items:

        if item["sourceName"] == source_name:
            return item["sceneItemId"]

    return None


def fit_source_to_canvas(cl, scene_name, item_id):
    """
    Scales the source to fit OBS canvas size.
    """

    video_settings = cl.get_video_settings()

    width = video_settings.base_width
    height = video_settings.base_height

    print(
        f"OBS canvas: {width}x{height}"
    )

    cl.set_scene_item_transform(
        scene_name=scene_name,
        item_id=item_id,
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


def setup_capture_source(cl, title, scene_name):
    """
    Creates and configures the Game Capture source.
    """

    source_name = "Game Capture"

    sources = get_scene_sources(
        cl,
        scene_name
    )

    if source_name not in sources:
        create_game_capture(
            cl,
            scene_name,
            source_name
        )

    print("Finding OBS window...")

    # Wait 30 seconds for window to appear.
    for i in range(30):
        window = get_game_window(
            cl,
            title
        )
        if(window):
            break

        time.sleep(5)



    if not window:
        raise Exception(
            f"Unable to find '{title}' in OBS window list"
        )

    print("Using OBS window:")
    print(window)

    update_game_capture(
        cl,
        source_name,
        window
    )

    return source_name


def obs_setup(
    host,
    port,
    password,
    title,
    timeout,
    use_dedicated_scene=True,
    dedicated_scene_name="clips",
):
    cl = connect_obs(
        host,
        port,
        password,
        timeout
    )

    if not use_dedicated_scene:
        return cl

    ensure_scene(
        cl,
        dedicated_scene_name
    )

    source_name = setup_capture_source(
        cl,
        title,
        dedicated_scene_name
    )

    item_id = get_scene_item_id(
        cl,
        dedicated_scene_name,
        source_name
    )

    if item_id is None:
        raise Exception(
            f"Could not find scene item {source_name}"
        )

    fit_source_to_canvas(
        cl,
        dedicated_scene_name,
        item_id
    )

    return cl



def start_replay_buffer(
    host,
    port,
    password,
    title,
    timeout,
    output_directory,
    use_dedicated_scene=True,
    dedicated_scene_name="clips",
):
    cl = obs_setup(
        host,
        port,
        password,
        title,
        timeout,
        use_dedicated_scene=use_dedicated_scene,
        dedicated_scene_name=dedicated_scene_name,
    )

    cl.set_profile_parameter(
        "Output",
        "RecFilePath",
        output_directory
    )

    status = cl.get_replay_buffer_status()

    if not status.output_active:
        print("Starting replay buffer...")
        cl.start_replay_buffer()

    return cl


def stop_replay_buffer(
    host,
    port,
    password,
    timeout,
):
    cl = connect_obs(
        host,
        port,
        password,
        timeout
    )

    status = cl.get_replay_buffer_status()
    if status.output_active:
        print("Stopping replay buffer...")
        cl.stop_replay_buffer()
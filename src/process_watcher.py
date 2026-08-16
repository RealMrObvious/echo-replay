import psutil
import keyboard
import time

def check_for_running_programs(program_list):
    """
    Checks all running processes against the configured program list.

    Args:
        program_list: List of program configurations containing executable paths.

    Returns:
        Tuple containing:
        - process ID
        - process name
        - window handle (HWND)

        Returns (None, None, None) if no program is found.
    """

    # Extract executable names from config and normalize to lowercase
    programs_list = [program["path"].lower() for program in program_list]

    # Iterate through all running processes
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = proc.info["name"]
            pid = proc.info["pid"]

            # Skip processes without a name
            if not name:
                continue

            # Check if the process matches a configured program
            if name.lower() in programs_list:
                print(f"Found {name} (PID: {pid})")

                # Return process information and its window handle
                return pid, name

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Process closed or access was denied while checking
            continue

    # No matching program was found
    return None, None

def check_running_program(pid,name):
    for proc in psutil.process_iter(["pid", "name"]):
        try:    
            # Skip processes without a name
            if proc.info["name"] != name or proc.info["pid"] != pid:
                continue
            else:
                return proc.info["pid"], proc.info["name"]

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Process closed or access was denied while checking
            continue
    
    # No matching program was found
    return None, None

def listen_for_hotkey(hotkey, clip_callback):
    keyboard.add_hotkey(
        hotkey,
        clip_callback
    )


def wait_for_game_open(games, thread):
    while not thread.isInterruptionRequested():
        pid, name = check_for_running_programs(games)

        if pid:
            return pid, name

        time.sleep(2)

    return None, None


def wait_for_game_close(pid, name, thread):
    while not thread.isInterruptionRequested():
        pid, name = check_running_program(pid, name)

        if pid is None:
            return

        time.sleep(2)

def get_process(pid):
    try:
        proc = psutil.Process(pid)
        return proc
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None

def popen_to_psutil_process(popen_obj):
    """
    Converts a subprocess.Popen object to a psutil.Process object.

    Args:
        popen_obj: A subprocess.Popen object.

    Returns:
        A psutil.Process object corresponding to the Popen object's PID.
    """
    return psutil.Process(popen_obj.pid)
import psutil

def check_for_running_games(games_list):
    """
    Checks all running processes against the configured game list.

    Args:
        games_list: List of game configurations containing executable paths.

    Returns:
        Tuple containing:
        - process ID
        - process name
        - window handle (HWND)

        Returns (None, None, None) if no game is found.
    """

    # Extract executable names from config and normalize to lowercase
    games_list = [game["path"].lower() for game in games_list]

    # Iterate through all running processes
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = proc.info["name"]
            pid = proc.info["pid"]

            # Skip processes without a name
            if not name:
                continue

            # Check if the process matches a configured game
            if name.lower() in games_list:
                print(f"Found {name} (PID: {pid})")

                # Return process information and its window handle
                return pid, name

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Process closed or access was denied while checking
            continue

    # No matching game was found
    return None, None

def check_running_game(pid,name):
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
    
    # No matching game was found
    return None, None
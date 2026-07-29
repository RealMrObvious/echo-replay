I updated it to match your current project features: tray app, hotkeys, automatic OBS startup, replay buffer workflow, window detection, and current config style.


# Echo Replay

Echo Replay is a lightweight automatic game clipping tool that detects running games, configures OBS automatically, and saves instant gameplay clips using the OBS Replay Buffer.

The goal is a ShadowPlay-style experience using OBS and the OBS WebSocket API.

## Features

- Automatically detects configured games
- Watches for games launching and closing
- Automatically starts and configures OBS
- Creates and manages a dedicated OBS capture scene
- Supports:
  - Game Capture
- Automatically finds the correct game window from OBS
- Automatically fits capture sources to the OBS canvas
- Uses OBS Replay Buffer for instant clips
- Global hotkey support for saving clips
- System tray application
- Runs quietly in the background

## Future Goals
- Compression/transcoding for discord sharing
- Automatic/bulk game searching
- improved gui/menu
- cleaner code
- installer/setup wizard
- linux/apple support (kinda already there? but untested)
- better setup guide/docs

## Requirements

- Windows
- Python 3.10+
- OBS Studio
- OBS WebSocket 5.x enabled
- Configured game list

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd clipping-software
````

Install dependencies:

```bash
pip install -r requirements.txt
```

## OBS Setup

### Enable OBS WebSocket

1. Open OBS Studio
2. Go to:

```
Tools → WebSocket Server Settings
```

3. Enable the WebSocket server

4. Configure:

```
Port: 4455
Password: Your password
```

### Enable Replay Buffer

In OBS:

```
Settings → Output → Replay Buffer → Enable Replay Buffer
```

Configure the replay length and recording settings to your preference.

## Configuration

Create or edit your configuration file:

```json
{
    "host": "localhost",
    "port": 4455,
    "password": "password",
    "hotkey": "ctrl+[",
    "obs_path": "C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe",
    "obs_timeout": 5,
    "use_dedicated_scene": true,
    "dedicated_scene_name": "clips",
    "output_directory": ".",
    "games": [
        {
        "name": "CS2",
        "path": "cs2.exe"
        }
    ]
}
```

## Usage

Run:

```bash
python src/main.py
```

Echo Replay will:

1. Start OBS
2. Start the tray application
3. Register the clip hotkey
4. Wait for a configured game to launch
5. Detect the game window
6. Configure OBS Game Capture
7. Start the Replay Buffer
8. Wait for hotkey input

Press your configured hotkey to save a replay.

Example:

```
CTRL+[
```

## Capture Modes

### Game Capture

Captures a specific game window through OBS Game Capture.

Recommended for:

* Games
* DirectX applications
* OpenGL applications

Echo Replay automatically searches OBS's available Game Capture windows and selects the matching process.

### Monitor Capture

Captures an entire monitor.

Recommended for:

* Games that do not support Game Capture
* Emulators
* Applications with unusual rendering methods

## Project Structure

```
src/
├── main.py              # Application entry point and game watcher
├── gui.py               # Tray icon and hotkey handling
├── obs_control.py       # OBS WebSocket control
├── process.py           # Process detection and window handling
├── config.py            # Configuration loading
└── media/               # Notification sounds/assets

requirements.txt         # Python dependencies
```

## Troubleshooting

### OBS does not capture the game

Try:

* Running OBS as administrator
* Running the game before starting capture
* Switching capture methods
* Using Monitor Capture instead
* Checking that the executable name matches your config

Example:

```json
{
    "path": "game.exe"
}
```

must match the running process name.

---

### Replay Buffer does not save clips

Check:

```
OBS → Settings → Output → Replay Buffer
```

Make sure:

* Replay Buffer is enabled
* The save location exists
* OBS has permission to write files

---

### Game window is not detected

Echo Replay relies on OBS's Game Capture window list.

Try:

* Waiting a few seconds after launching the game
* Checking that OBS can manually capture the game
* Running OBS before launching the game

---

## License

```
Personal project.
Use and modify as needed.
```

## AI Disclosure


```
Documentation and comments were assisted by AI. All code and project implementation were written by me.
```

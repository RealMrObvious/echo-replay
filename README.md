# Echo Replay

Echo Replay is a lightweight automatic game clipping tool that detects running games, configures OBS automatically, and saves instant gameplay clips using the OBS Replay Buffer.

The goal is a ShadowPlay-style/steelseries moments experience using OBS and the OBS WebSocket API.

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

### [Getting Started](./docs/getting-started.md)

### [Troubleshooting](./docs/faq.md)


## Codebase Installation

Clone the repository:

```bash
git clone <repository-url>
cd echo-replay
````

Install dependencies:

```bash
pip install -r requirements.txt
```

If you dont have [OBS](https://obsproject.com/) installed, you will need to install it. Launch OBS and follow the [OBS setup](./docs/getting-started.md/#obs-setup). When finished, exit out of OBS.

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

### Game Capture

Captures a specific game window through OBS Game Capture.

Recommended for:

* Games
* DirectX applications
* OpenGL applications

Echo Replay automatically searches OBS's available Game Capture windows and selects the matching process.

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

## License

```
Personal project.
Use and modify as needed.
```

## AI Disclosure


```
Documentation and comments were assisted by AI. All code and project implementation were written by me.
```

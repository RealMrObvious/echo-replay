````markdown id="59381"
# Echo

Echo is a lightweight game clipping tool that automatically detects running games and uses OBS to capture gameplay through the OBS WebSocket API.

## Features

- Detects when configured games are running
- Creates and manages an OBS capture scene
- Supports:
- Game Capture
- Automatically fits capture sources to the OBS canvas
- Uses OBS Replay Buffer for instant clips
- Designed to run quietly in the background

## Requirements

- Windows
- Python 3.10+
- OBS Studio
- OBS WebSocket enabled
- Configured games list

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

1. Open OBS Studio
2. Go to:

```
Tools → WebSocket Server Settings
```

3. Enable the WebSocket server

4. Set:

   * Port *(default should be `4455`)*
   * Password *(optional)*

5. Enable Replay Buffer:

```
Settings → Output → Replay Buffer → Enable Replay Buffer
```

## Configuration

Create/edit your config file:

```json
{
    "host": "localhost",
    "port": 4455,
    "password": "password",
    "fps": 60,
    "games": [
        {
            "name": "Rivals of Aether",
            "path": "RivalsofAether.exe"
        }
    ]
}
```

## Usage

Run:

```bash
python src/main.py
```

The program will:

1. Search for configured games
2. Find the game window
3. Create/update the OBS capture source
4. Start the Replay Buffer

## Capture Modes

### Game Capture

Captures the selected game window.

Recommended for:

* Games
* DirectX/OpenGL applications

### Monitor Capture (WIP)

Captures an entire display.

Recommended for:

* Games that do not work with Game Capture
* Emulators
* Desktop applications

## Project Structure

```
src/
├── main.py                 # Application entry point
├── capture.py              # Capture logic
├── obs_control.py          # OBS WebSocket control
├── process.py              # Process/window detection
example-config.py           # Configuration handling
```

## Troubleshooting

### OBS does not capture the game

Try:

* Switching between Game Capture and Monitor Capture
* Running OBS as administrator
* Checking the window title/class
* Changing the OBS capture method to Windows Graphics Capture

### Replay Buffer will not start

Make sure:

```
OBS → Settings → Output → Replay Buffer
```

is enabled.

## License

```
Personal project. Use and modify as needed.
```

## AI Disclosure

Most comments/documentation are AI generated however all code is written by me.
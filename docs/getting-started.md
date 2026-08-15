# Getting Started

## After running the installer but before opening the app.

1. If you dont have [OBS](https://obsproject.com/) installed, you will need to install it.
2. Launch OBS and follow the [OBS setup](#obs-setup). When finished, exit out of OBS.
3. Go to where you installed Echo Replay and edit your [configuration file](#configuration-file).

## OBS Setup

### Enable OBS WebSocket

1. Open OBS Studio
2. Go to:

```
Tools → WebSocket Server Settings
```

3. Enable the WebSocket server

4. Configure:

```bash
Port: 4455
# 4455 should be the default.

Password: Your password
# You can also disable authentication if you wish
```
5. Click apply & ok

### Enable Replay Buffer

In OBS:

```
File → Settings → Output → Replay Buffer → Enable Replay Buffer
```

Configure the replay length and recording settings to your preference (*default 20s*).

### Configuring Capture Settings

In OBS:

```
File → Settings → Video
```

Here you can configure the output resolution as well as the capture frame rate.

Capture frame rates are generally not recomended/ not encouraged by OBS.


## Configuration File

This configuration file controls the connection to OBS Studio, the clipping hotkey, where clips are saved, and which games the application monitors. Your `config.json` will be in the directory you chose to install echo_replay to.

 *In the future this will be handled via gui but for now is a file.*

### Configuration Options

| Option                 | Example                                                  | Description                                                                                     |
| ---------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `host`                 | `"localhost"`                                            | The address where OBS Studio is running. `localhost` means OBS is running on the same computer. |
| `port`                 | `4455`                                                   | The port used to connect to OBS WebSocket. `4455` is the default OBS WebSocket port.            |
| `password`             | `"password"`                                             | The OBS WebSocket authentication password. This must match the password configured in OBS. If OBS Websocket authentication is disabled, this can be whatever.      |
| `hotkey`               | `"ctrl+["`                                               | Keyboard shortcut used to trigger a clip.                                                       |
| `obs_path`             | `"C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe"` | Full path to the OBS Studio executable. This should be configured automatically via the installer but can be set manually if needed.                                                         |
| `obs_timeout`          | `5`                                                      | Number of seconds the application waits when connecting to or starting OBS.                     |
| `use_dedicated_scene`  | `true`                                                   | Enables the use of a separate OBS scene specifically for clips.                                 |
| `dedicated_scene_name` | `"clips"`                                                | Name of the OBS scene used when creating clips. The scene should exist in OBS.                  |
| `output_directory`     | `"."`                                                    | Directory where clips are saved. `.` means the application's current working directory.         |
| `games`                | `[...]`                                                  | List of games that the application can detect and monitor.                                      |
| `games[].name`         | `"CS2"`                                                  | Display/name identifier for the game.                                                           |
| `games[].path`         | `"cs2.exe"`                                              | Executable filename used to identify the game process.                                          |

### Example Configuration

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
        },
        {
            "name": "CS3",
            "path": "cs3.exe"
        },
        {
            "name": "SSF2",
            "path": "SSF2.exe"
        }
    ]
}
```

### Adding Another Game

Additional games can be added to the `games` array:

```json
"games": [
    {
        "name": "CS2",
        "path": "cs2.exe"
    },
    {
        "name": "Example Game",
        "path": "game.exe"
    }
]
```

Each game requires a unique `name` and the executable filename in `path`.

### Important Notes about `config.json`

* Windows paths in JSON require escaped backslashes (`\\`).
* JSON requires **double quotes** around strings.
* Do not add a trailing comma after the final property.
* If you change the OBS WebSocket port or password, update the configuration accordingly.

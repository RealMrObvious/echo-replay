# FAQ

### OBS does not capture the game

Try:

- Running OBS as administrator
- Running the game before starting capture
- Switching capture methods
- Using Monitor Capture instead
- Checking that the executable name matches your config

Example:

```json
{
 "path": "game.exe"
}
```

### Clips are fully black/white or sound is muted

- CS2 requires whitelisting OBS ([guide](https://help.steampowered.com/en/faqs/view/09A0-4879-4353-EF95#whitelist))
- Check that the correct audio device is selected in OBS
- Make sure the game is not muted in the Windows Volume Mixer
- Try disabling overlays or other capture software that may conflict with OBS
- If using Game Capture, try running OBS as administrator

### Replay Buffer does not save clips

Check:

```
OBS → Settings → Output → Replay Buffer
```

Make sure:

- Replay Buffer is enabled
- The save location exists
- OBS has permission to write files
- There is enough free disk space
- The replay buffer duration is long enough

### Game window is not detected

Echo Replay relies on OBS's Game Capture window list.

Try:

- Waiting a few seconds after launching the game
- Checking that OBS can manually capture the game
- Running OBS before launching the game
- Recreating the Game Capture source
- Making sure the correct game executable/window is selected
- Restarting OBS after changing the game's launch state

### OBS is dropping frames or clips are stuttering

Try:

- Lowering the recording/replay-buffer quality
- Reducing the output resolution or FPS
- Using a hardware encoder such as NVENC, AMF, or QuickSync
- Closing applications that heavily use the CPU or GPU
- Running OBS as administrator
- Checking OBS's Stats window for rendering or encoding lag

### OBS crashes or becomes unresponsive

Try:

- Updating OBS to the latest version
- Updating your GPU drivers
- Disabling recently installed OBS plugins
- Removing recently added browser, capture, or third-party plugins
- Running OBS as administrator
- Checking the OBS log for errors

### Echo Replay cannot communicate with OBS

Try:

- Confirming that OBS is running
- Checking that WebSocket is enabled
- Verifying that the configured port matches the OBS WebSocket port
- Checking that the password matches
- Restarting OBS and Echo Replay
- Checking whether a firewall is blocking the connection

### OBS works manually but Echo Replay does not

If OBS can capture the game normally but Echo Replay cannot:

- Verify that Echo Replay is connected to the correct OBS instance
- Check that the expected Game Capture source exists
- Confirm that the game executable matches your Echo Replay configuration
- Restart both OBS and Echo Replay
- Check the Echo Replay and OBS logs for connection or source errors
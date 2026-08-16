# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] - 2026-08-15

### Added
- created new docs ([Getting Started](./docs/getting-started.md) and [FAQ](./docs/faq.md)) 
- Echo replay will attempt to connect to an already open instance of OBS rather than always opening a new process

### Changed

- updated to `pyQT6`
- directory is now set at connection time, not start replay buffer time
- updated readme
- The input source is no longer named `Game Capture`, but instead `Game Capture - Echo Replay`
- The dedicated scene is no longer named `clips`, but instead `Clips - Echo Replay`

### Fixed
- **requirements.txt** removed invalid requirement
- handling of invalid directories was improved
- disabled replay buffer errors are now caught 



## [0.2.1] - 2026-08-13

### Changed

- **requirements.txt** has been updated/cleaned up

### Fixed
- Exe no longer crashes due to missing `pyQT5`

## [0.2.0] - 2026-08-12

### Added
- Now chimes when a game you've started/stopped a targeted game
- Replay buffer automatically disables when no game is detected (very nice for saving on memory.)
- Settings button in tray auto opens config.json (must restart app to see changes)

### Changed 
- switched from pstray -> QT to allow for more expansion of GUI options
- refactored most code to simply be better/in a more OOP style.

## [0.1.4] - 2026-07-30

### Changed 
- Changed exe name 
- Changed build to mark alpha builds as pre-release

## [0.1.3] - 2026-07-30

### Added
- created a new installer using Inno

### Fixed
- changed build.bat -> build.ps1
- updated gh workflows to follow suit.

## [0.1.2] - 2026-07-30

### Added
- added gh workflows + build scripts
- new icon.ico

## [0.1.1] - 2026-07-29

### Added
- added `config.json` to .gitignore

### Fixed
- output directory now works properly
- config.py now targets `config.json` not `example-config.json`

## [0.1.0] - 2026-07-29

### Added 

- Initial Creation lol.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2029-08-13

### Changed

- **requirements.txt** has been updated/cleaned up

### Fixed
- Exe no longer crashes due to missing `pyQT5`

## [0.2.0] - 2029-08-12

### Added
- Now chimes when a game you've started/stopped a targetted gane
- Replay buffer automatically disables when no game is detected (very nice for saving on memory.)
- Settings button in tray auto opens config.json (must restart app to see changes)

### Changed 
- switched from pstray -> QT to allow for more expansion of GUI options
- refactored most code to simply be better/in a more OOP style.

## [0.1.4] - 2029-07-30

### Changed 
- Changed exe name 
- Changed build to mark alpha builds as pre-release

## [0.1.3] - 2029-07-30

### Added
- created a new installer using Inno

### Fixed
- changed build.bat -> build.ps1
- updated gh workflows to follow suit.

## [0.1.2] - 2029-07-30

### Added
- added gh workflows + build scripts
- new icon.ico

## [0.1.1] - 2029-07-29

### Added
- added `config.json` to .gitignore

### Fixed
- output directory now works properly
- config.py now targets `config.json` not `example-config.json`

## [0.1.0] - 2029-07-29

### Added 

- Initial Creation lol.
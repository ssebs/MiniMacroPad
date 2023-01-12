# MiniMacroPad

Keyboard firmware and driver for my macropad. Using a Arduino Pro Micro

## Firmware / arduino stuff
See `MiniMacroPad.ino` for more details, but basically you click a button and it sends a serial number of what button you pressed

### Grid
Here's what the grid looks like physically:
```
[1] [2]
[3] [4]
```


## driver
A python driver to provide functionality to the mini macro pad.

## Install dependencies
- python3
- `cd driver/`
    - `python3 -m venv venv`
    - `.\venv\Scripts\Activate.ps1`
    - `pip install -r requirements.txt`

### Building the .exe
- `cd driver/`
- `pyinstaller minimacropad.spec`
    - Built file is under `./dist/`

## TODO:
- [ ] Make driver work
- [ ] Functional actions / macros
  - [ ] Keyboard macros
  - [ ] Mouse macros
  - [ ] Other stuff?
- [ ] JSON customizable actions (or YAML)
  - [ ] EZ edit for these

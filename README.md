# MiniMacroPad

Keyboard firmware and driver for my macropad. Using a Arduino Pro Micro or teensy lc in my case.

The goal of this project is to have a physical macro pad that you can customize. You can set keyboard/mouse macros with it for general use, and it supports not having the physical buttons too if you don't have the hardware.

See [my thangs.com model](https://thangs.com/designer/sebsafari/3d-model/Mini%20Macro%20Pad-710028?manualModelView=true) for the related STL files that you can print.

## Firmware / arduino stuff
See `MiniMacroPad.ino` for more details, but basically you click a button and it sends a serial number of what button you pressed. For this example the macropad is a 2x2 layout.

### Grid
Here's what the grid looks like physically:
```
[1] [2]
[3] [4]
```

## Driver (GUI)
A python driver to provide functionality to the mini macro pad. All driver related code is under the `driver/` folder.

## Install dependencies
- python3
- `cd driver/`
    - `python3 -m venv venv`
    - `.\venv\Scripts\Activate.ps1`
      - This is for windows
    - `pip install -r requirements.txt`

### Building the .exe
- `cd driver/`
- `pyinstaller minimacropad.spec`
    - Built file is under `./dist/`
    - Run this .exe

#### Running at startup
- Hit `WIN + R`
  - Enter `shell:startup` in the dialog, hit enter to open the folder
  - Copy the .exe file to this folder

### Running in dev
- Once in a virtual environment (venv)
  - `python3 driver/minimacropad.py`
- If you'd like to enable verbosity, replace the `DEBUG` variable in `minimacropad.py`.
  - > This will be updated... at some point

## Config file
There is a `C:\Users\<username>\minimacropad-config.json` file that controls the configuration of the macro pad. See [CONFIG.md](./CONFIG.md) for more details.

## Screenshot of GUI
This may be out of date.
![screenshot](./img/mmpscreenshot.png)

## Hardware
You'll need an arduino with some buttons. 
Screenshot of mine below:
![macro pad](./img/mmpbuilt.png)

TBD: wiring diagram
![wiring](./img/mmpwiring.png)
TBD: better instructions

## LICENSE
[GPL v3](./LICENSE)

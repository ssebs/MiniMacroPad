# MiniMacroPad

Keyboard firmware and driver for my macropad. Using a Arduino Pro Micro or teensy lc in my case.

See [thangs.com](https://thangs.com/designer/sebsafari/3d-model/Mini%20Macro%20Pad-710028?manualModelView=true) for the related STL files that you can print.

## Firmware / arduino stuff
See `MiniMacroPad.ino` for more details, but basically you click a button and it sends a serial number of what button you pressed

### Grid
Here's what the grid looks like physically:
```
[1] [2]
[3] [4]
```

## driver
A python driver to provide functionality to the mini macro pad. All driver related code is under driver.

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
    - Run this .exe

## Config file
A config file that controls the macro pad will be created for you. This will be saved in your `home directory/minimacropad-config.json`.

- Windows:
  - `C:\Users\<username>\minimacropad-config.json`
- *nix:
  - `~/minimacropad-config.json`

*This json file is how you will control the functionality of the macro pad.*

There's an expected format for this file:
- A `DATA` object where you can add lists of strings that you may want to use for looping thru.
  - Like: `"DATA": { "ARR_NAME": ["value1", "value2"] }`
- A `BUTTONS` object where you'll need the following attributes:
  - `pos`
    - int, position of the button. idx + 1 basically
  - `text`
    - string, text to render or send depending on function
  - `func`
    - string, name of the function to run
    - Possible functions are:
      - `send_text`
        - Types whatever is in the "text" field
      - `send_hotkey`
        - Types whatever you put in the array, supports multiple hotkeys
        - e.g.  `[ [ "win", "r" ], [ "TXT=shell:startup", "enter" ] ]`
        - What you enter here needs to work with `keyboard.press`
          - If adding a string value in the hotkey, add `TXT=` before.
            - e.g. `"TXT=shell:startup"`
      - `loop_up`
        - Types whatever is up next in the loop
        - Requires `extra` to be definied 
      - `loop_down`
        - Types whatever was last in the loop
        - Requires `extra` to be definied 
      - `loop_rand`
        - Types random place in the loop
        - Requires `extra` to be definied 
  - `extra`
    - string, extra metadata that may be required.
    - Example is name of the list of strings that will be used to loop thru
  - `pre`
    - Runs before the main function, takes same params as hotkeys
  - `post`
    - Runs after the main function, takes same params as hotkeys

> See ./driver/res/sampleconfig.json for detailed example

## Screenshot of GUI
This may be out of date.
![screenshot](./img/mmpscreenshot.png)

## TODO:
- [ ] Support delays!
- [ ] Mouse macros
- [ ] Editor GUI for config file?
  - [ ] Support ez features from json
  - [ ] Support all features from json
- [ ] Cleanup GUI, same size buttons
- [ ] Support audio stuff?
  - [ ] i.e. soundboard and hold press to talk at the same time?
- [ ] Display next/last looper var in gui, don't just show next
- [ ] Support encrypted files
- [ ] Support multi-button macros
- [ ] Support hotkeys + using Serial data?
- [ ] Move extra btns to new row
- [ ] Support multiple pages of stuff

## Tech Debt
- [ ] Stop using global vars
- [ ] Rename lots of variables
  - [ ] "Util" class 🙄
  - [ ] "thread1"
  - [ ] handle_press in MacroDisplay
  - [ ] click in MacroDisplay
- [ ] Some testing?
- [ ] Wiring diagram?

## Completed work (moved from todo or TD)
- [x] Fix shift + enter
- [x] Add pre and post wrapper functions to all
- [x] config file for macropad settings
- [x] JSON customizable actions (or YAML)
  - [x] make this save / load to ~/minimacropad-config.json
- [x] Make driver work
- [x] Functional actions / macros
  - [x] Keyboard macros
- [x] support multiple pads (in config at least)
- [x] Pics of my arduino
- [x] Support clicking on gui button to do macro
- [x] Stop using `pos` variable (fix positioning / indexing)

## Hardware
You'll need an arduino with some buttons. 
Screenshot of mine below:
![macro pad](./img/mmpbuilt.png)

TBD: wiring diagram
![wiring](./img/mmpwiring.png)
TBD: better instructions

## LICENSE
[GPL v3](./LICENSE)

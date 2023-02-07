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

## Config file
You'll need to create a config file that controls the macro pad. This will be saved in your `home directory/minimacropad-config.json`
  - Windows:
    - `C:\Users\<username>\minimacropad-config.json`
  - *nix:
    - `~/minimacropad-config.json`

There's an expected format for this file:
- A `DATA` object where you can add lists of strings that you may want to use.
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
      - `send_undo`
        - Types CTRL + Z
      - `send_hotkey`
        - Types whatever you put in the array, supports multiple hotkeys
        - e.g.  `[ [ "win", "r" ], [ "shell:startup", "enter" ] ]`
        - What you enter here needs to work with `pyautogui.hotkey()`
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

> See the example below for clarification / usage
> 
Example below:
```json
{
  "DATA": {
    "FRUITS": [
      "banana",
      "apple",
      "orange"
    ],
    "NAMES": [
      "Sebastian",
      "Tom",
      "Bob"
    ]
  },
  "BUTTONS": [
    {
      "pos": 1,
      "text": "Fruit down",
      "func": "loop_down",
      "extra": "FRUITS",
      "pre": [
          [
              "shift",
              "enter"
          ]
      ],
      "post": [
          [
              "enter"
          ]
      ]
    },
    {
      "pos": 2,
      "text": "Foo\n",
      "func": "send_text"
    },
    {
      "pos": 3,
      "text": "Fruit up",
      "func": "loop_up",
      "extra": "FRUITS",
      "post": [
          [
              "enter"
          ]
      ]
    },
    {
      "pos": 4,
      "text": "Startup Folder",
      "hotkeys": [
          [
              "win",
              "r"
          ],
          [
              "shell:startup",
              "enter"
          ]
      ],
      "func": "send_hotkey"
    },
    {
      "pos": 5,
      "text": "Undo",
      "hotkeys": [
          [
              "ctrl",
              "z"
          ]
      ],
      "func": "send_hotkey"
    },
    {
      "pos": 6,
      "text": "Rand Name",
      "func": "loop_rand",
      "extra": "NAMES"
    },
  ]
}
```

## TODO:
- [x] Make driver work
- [x] Functional actions / macros
  - [x] Keyboard macros
  - [ ] Mouse macros
  - [ ] Other stuff?
- [...] JSON customizable actions (or YAML)
  - [x] make this save / load to ~/minimacropad-config.json
  - [ ] EZ edit for these
- [ ] Editor GUI for config file
  - [ ] How many buttons?
  - [ ] How many cols?
  - [ ] Serial Device name
  - [ ] Enter lists for loopers
  - [ ] Select predefinied functions
- [ ] new GUI
- [ ] support multiple pads (in config at least)
- [ ] support multiple pages of stuff
- [ ] support delays in macros
- [ ] support clicking on gui button to do macro
- [ ] support audio stuff
  - [ ] i.e. soundboard and hold press to talk at the same time

https://ttkbootstrap.readthedocs.io/en/latest/themes/dark/
# Config file

A config file that controls the macro pad will be created for you. This will be saved to `C:\Users\<username>\minimacropad-config.json` 

*This json file is how you will control the functionality of the macro pad!*

## GUI
I'd like to create a GUI to edit the macros, but we're not there yet. So for now you have to edit JSON.

## There's an expected format for this JSON file:
> Note: this may change at a later date!

> See ./driver/res/sampleconfig.json for detailed example with the LATEST updates!

- `CONFIG`
  - `SIZE` (Rows/Cols for splitting up the buttons)
    - `x` - how many columns in int
    - `y` - how many rows in int
  - `GUI_SIZE` (Size of the window)
    - Expects a string in the format "\<pixels-wide\>x\<pixels-tall\>"
    - Example: `500x300`
  - `MONITOR` (Which monitor to open the GUI on.)
    - Expects an int Example: `1`
  - `SERIAL` (Serial data)
    - `QUERY` (Name of the serial device (Arduino))
      - Expects a str
    - `BAUDRATE`
      - Expects an int
    - `TIMEOUT` (Serial timeout)
      - Expects a float
  - `RETRY_COUNT` (How many times to retry connecting to the serial device)
- `DATA` (Add lists of strings for use with loopers)
  - Example:
    ```json
    {
      "FRUITS": [
        "banana",
        "apple",
        "orange"
      ]
    }
    ```
- `ACTIONS` (Dict of actions (macros)):
  - Expects:
    - A list of action objects
    - Action object:
      - REPLACE_ME_PLS_DEV
  - Action object Example:
    ```json
    "Undo": [
      {
        "KB_SEND_HOTKEY": [
          "ctrl",
          "z"
        ]
      }
    ],
    ```
  - Typically, you'd use multiple:
    - Example:
      ```json
      "Open Startup Folder": [
        {
          "KB_SEND_HOTKEY": [
            "windows",
            "r"
          ]
        },
        {
          "DELAY": 0.2
        },
        {
          "KB_SEND_STR": "shell:startup"
        },
        {
         "DELAY": 0.2
        },
        {
          "KB_KEY_PRESS": "enter"
        }
      ],
      ```
- You'd add both of these examples together to have 2 buttons (Example):
  ```json
  "ACTIONS": {
    "Undo": [
      {
        "KB_SEND_HOTKEY": [
          "ctrl",
          "z"
        ]
      }
    ],
    "Open Startup Folder": [
      {
        "func": "KB_SEND_HOTKEY",
        "KB_SEND_HOTKEY": [
          "windows",
          "r"
        ]
      },
      {
        "DELAY": 0.2
      },
      {
        "KB_SEND_STR": "shell:startup"
      },
      {
        "DELAY": 0.2
      },
      {
        "KB_KEY_PRESS": "enter"
      }
    ]
  }
  ```
## Available Functions:
- The key name can be any of:
  - `DELAY` (time delay)
    - `value` (how long in seconds (0.2)) type: float 
  - `KB_SEND_HOTKEY`
    - `value` (keyboard press a hotkey. (["alt", "tab"])) type: List[str]
  - `KB_SEND_STR`
    - `value` (keyboard send a word/sentence/string. (ggwp)) type: str
  - `KB_SEND_LOOP_UP`
    - `value` TODO: Explain this
  - `KB_SEND_LOOP_DOWN`
    - `value` TODO: Explain this
  - `KB_SEND_LOOP_RAND`
    - `value` TODO: Explain this
  - `KB_KEY_PRESS`
    - `value` (keyboard press and release a key ("enter")) type: str
  - `KB_KEY_DOWN`
    - `value` (keyboard hold a key down ("ctrl")) type: str
  - `KB_KEY_UP`
    - `value` (keyboard release a key ("ctrl")) type: str
  - `MOUSE_CLICK`
    - `value` This is not implemented
  - `MOUSE_DOWN`
    - `value` This is not implemented
  - `MOUSE_UP`
    - `value` This is not implemented
  - `MOUSE_MOVE_TO`
    - `value` This is not implemented
  - `MOUSE_RECORD`
    - `value` This is not implemented

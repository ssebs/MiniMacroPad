# Config file

A config file that controls the macro pad will be created for you. This will be saved to `C:\Users\<username>\minimacropad-config.json` 

*This json file is how you will control the functionality of the macro pad.*

## There's an expected format for this file:
> Note: this may change at a later date

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
- `ACTIONS` object:
  - What to support:
    - [] delay
    - [] keyboard hotkey (alt+tab)
    - [] keyboard send string ("test\n")
    - [] keyboard send looper string ('ggez')
    - [] keyboard send key ("enter")?
      - could use press and hold
    - [] keyboard hold down
    - [] keyboard release
    - [] mouse click 
    - [] mouse hold down
    - [] mouse release
    - [] mouse move to pos
    - [ ] mouse record clicks
  - ACTION `type`'s:
    - `DELAY`,
    - `KB_SEND_HOTKEY`
    - `KB_SEND_STR`
    - `KB_SEND_LOOP`
    - `KB_KEY_PRESS`
    - `KB_KEY_DOWN`
    - `KB_KEY_UP`
    - `MOUSE_CLICK`
    - `MOUSE_DOWN`
    - `MOUSE_UP`
    - `MOUSE_MOVE_TO`
    - `MOUSE_RECORD`
  - 
> See ./driver/res/sampleconfig.json for detailed example
# Config file

A config file that controls the macro pad will be created for you. This will be saved to `C:\Users\<username>\minimacropad-config.json` 

*This json file is how you will control the functionality of the macro pad.*

## There's an expected format for this file:
> Note: this may change at a later date

- A `DATA` object where you can add lists of strings that you may want to use for looping thru.
  - Like: `"DATA": { "ARR_NAME": ["value1", "value2"] }`

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
  - All actions have a `value`!
> See ./driver/res/sampleconfig.json for detailed example
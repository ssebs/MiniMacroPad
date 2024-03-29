# TODO

List of work to be done for this project.

## MUST HAVE
- [x] Support delays!
- [ ] Config file button/action rework
  - [x] delay
  - [x] keyboard hotkey (alt+tab)
  - [x] keyboard send string ("test\n")
  - [ ] keyboard send looper string ('ggez')
  - [x] keyboard send key ("enter")?
  - [x] keyboard hold down
  - [x] keyboard release
  - [ ] mouse click 
  - [ ] mouse hold down
  - [ ] mouse release
  - [ ] mouse move to pos
- [ ] Support recording
  - [ ] mouse record clicks & positions
  - [ ] keyboard record presses
  - [ ] GUI for recording
- [ ] Mouse macros
  - [ ] Playback mouse macro
  - [x] Allow keyboard + mouse at the same time (config file)
- [ ] Editor GUI for config file?
  - [ ] Support ez features from json
  - [ ] Support all features from json
- [ ] Cleanup GUI, same size buttons
- [ ] CLI args 
  - [ ] verbose
  - [ ] no arduino mode

## Tech Debt
- [ ] Stop using global vars
- [ ] Continue refactor to simplify the code
- [ ] Fix `python -m mmp` not working
- [ ] # TODO's
- [ ] Some testing?
- [ ] Wiring diagram?

## Wish list if I happen to get to it
- [ ] Support audio stuff?
  - [ ] i.e. soundboard and hold press to talk at the same time?
- [ ] Display next/last looper var in gui, don't just show next?
- [ ] Support encrypted files
- [ ] Support multi-button macros
- [ ] Support hotkeys + using Serial data?
- [ ] Move extra btns to new row
- [ ] Support multiple pages of stuff

## Completed work (moved from todo or TD)
- [x] Change how the pre/func/post works
  - [x] pre/post only allow for holding keys
  - [x] not easy to support mouse
- [x] Fix Exception: Failed to find ./res/sampleconfig.json error
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
- [x] Refactor / cleanup pt 1
- [x] Rename lots of variables
  - [x] "Util" class 🙄
  - [x] handle_press in MacroDisplay
  - [x] click in MacroDisplay
#!/usr/bin/env python3
# macromanager.py - Manager for the Macros for use with the MiniMacroPad
import keyboard
import mouse
import time

from datetime import datetime
from enum import Enum
from tkinter import Tk
from typing import Tuple, Dict, List, Any

from config import Config
from stringlooper import StringLooper
from actionmanager import ActionManager


class FuncManager():
    """The actual functionality for the Macros
    TODO: Move to own file
    """

    def __init__(self, config: Config, default_delay: float = 0.2, verbose: bool = False):
        self.verbose: bool = verbose
        self.config: Config = config
        self.default_delay: float = default_delay
        self.loopers: Dict[StringLooper] = self._parse_loopers()
    # __init__

    def _parse_loopers(self) -> dict:
        """parse config json to create string loopers
        (Instantiates StringLooper objects)
        Returns:
            dict[str, StringLooper]
        """
        # TODO: fix the exception handling! make it return an error instead of raising here
        _looper = {}
        # TODO: reimplement
        for btn in self.config.buttons:
            if "extra" not in btn:
                continue
            try:
                # If the array name is not in data
                if btn["extra"] not in self.config.data:
                    raise Exception(
                        f"Failed to find {btn['extra']} in {self.config.data}")
                # Get array name from extra variable
                tmp_loop = StringLooper(self.config.data[btn['extra']])
                # Add to dict
                _looper[btn['extra']] = tmp_loop

            except Exception as e:
                print("Failed to add looper")
                raise e

        if self.verbose:
            print("loopers:")
            for looper in _looper.values():
                print(looper)

        # Return new dict
        return _looper
    # _parse_loopers

    def run_alt_tab(self, delay: float = None):
        _delay = delay if delay else self.default_delay
        self._press_and_hold(["alt", "tab"])
        time.sleep(_delay)

    def _press_and_hold(self, keys: list, delay: float = None):
        """Takes a list of keys to hold at the same time
        Params:
            keys - list, list of keys to hold simultaneously
            delay - float, how long in seconds to hold the keys down. Default to self.default_delay
        """
        # Set to default if undefined
        # TODO: confirm this is the same as the other one that's similar...
        _delay = delay if delay else self.default_delay

        # Press all keys down
        for key in keys:
            # If we are sending a string, use write instead
            if key.startswith("TXT="):
                keyboard.write(key[4:])
                time.sleep(_delay)
            else:
                keyboard.press(key)
        # Wait
        time.sleep(_delay)
        # Release all keys
        for key in keys:
            # Ignore releasing strings
            if not key.startswith("TXT="):
                keyboard.release(key)
    # _press_and_hold

    def prepost(func):
        """wrapper function"""
        def outware(*args):
            self = args[0]
            _idx = args[1]

            if "pre" in self.config.buttons[_idx]:
                for keys in self.config.buttons[_idx]["pre"]:
                    if self.verbose:
                        print(f"pre - pressing {'+'.join(keys)}")
                    self._press_and_hold(keys)
            func(*args)
            if "post" in self.config.buttons[_idx]:
                for keys in self.config.buttons[_idx]["post"]:
                    if self.verbose:
                        print(f"post - pressing {'+'.join(keys)}")
                    self._press_and_hold(keys)
        return outware
    # wrapper func to handle pre/post hotkeys

    # # All send_<blah> functions should be exposed to the user somehow, this is what they'll put in the configs # #

    @prepost
    def send_text(self, idx: int):
        keyboard.write(self.config.buttons[idx]["text"])
    # send_text

    @prepost
    def send_hotkey(self, idx: int):
        # TODO: fix exception
        if "hotkeys" not in self.config.buttons[idx]:
            raise Exception(f"Hotkeys not defined in BUTTONS[{idx}]")

        for keys in self.config.buttons[idx]["hotkeys"]:
            self._press_and_hold(keys)
    # send_hotkey func from json

    @prepost
    def loop_up(self, idx: int, extra: str):
        self.loopers[extra].loop_up()
        if self.verbose:
            print(
                f"loop_up: {self.loopers[extra].get_str()}, idx: {idx}, extra: {extra}")
        keyboard.write(self.loopers[extra].get_str())
    # loop_up func from json

    @prepost
    def loop_down(self, idx: int, extra: str):
        self.loopers[extra].loop_down()
        keyboard.write(self.loopers[extra].get_str())
    # loop_down func from json

    @prepost
    def loop_rand(self, idx: int, extra: str):
        self.loopers[extra].loop_rand()
        keyboard.write(self.loopers[extra].get_str())
    # loop_rand func from json

# FuncManager


class MacroManager():
    """
    Manager for the Macros for use with the MiniMacroPad
    (Instantiates Config, FuncManager objects)
    Params:
        root_win - Tk, root container
        config_path - str [None], path to config, if None use default
        verbose - bool [False], verbosity
    Methods:
        run_action
    """

    def __init__(self, root_win: Tk, config_path: str = None, verbose: bool = False):
        self.verbose: bool = verbose
        # Load json Config from file, takes config_path if provided
        self.config: Config = Config(config_path=config_path, verbose=verbose)

        self.action_manager: ActionManager = ActionManager(self.config, verbose=verbose)

        # self.func_manager: FuncManager = FuncManager(
        #     config=self.config, verbose=verbose)

        # Set root_win from param
        self.root_win: Tk = root_win

        # TODO: replace this comment
        self.last_pressed_pos = -1
        self.delay = 0.02  # seconds
    # __init__

    def run_action(self, position: int = -1, action_name: str = None, value: Any = None):
        """Run an action depending on the action type
        TODO: reimplement this to use ACTIONS instead of BUTTONS
        Params:
            position - int [-1], position where to call the action function from
        """
        if self.verbose:
            print(f"Running button press for {position}")
        
        # Run action_name if defined, don't use the button position at all!
        if action_name:
            if value is None:
                raise Exception(f"Value cannot be None for {action_name}")
            self.action_manager.actions[action_name](value)
            return

        self.last_pressed_pos = position

        action_name, action_items = self._get_action_from_pos()
        # For every action in action_items, run the func
        for action in action_items:
            # action: Dict[str, any]
            func_name = action["func"]
            func_value = action["value"]
            self.action_manager.actions[func_name](func_value)

        # # Get function name from position within buttons[] from config
        # func_name, extra = self._get_func_from_pos()
        # # Print error if there is one and return
        # if func_name is None or func_name == "err":
        #     print(extra)
        #     return
        # # TODO: support mouse recording
        # # Actually run the function, must be defined in FuncManager
        # # TODO: try/catch
        # self._run_func_from_name(func_name, extra)
        # # TODO: add recording action!
        
    # run_action

    def rec_mouse(self, idx: int):
        """Record mouse inputs"""
        positions: Dict[str, str] = {}
        has_quit: bool = False
        count: int = 0

        def add_pos(_type: str):
            # Add mouse position and button click to positions
            # _type can be: left, right, double, middle
            x, y = mouse.get_position()
            now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%Z")
            positions[str(now)] = {
                "type": _type,
                "posx": x,
                "posy": y,
            }

        while not has_quit and count < 999999999:
            # Record user input until they hit "ESC"
            count += 1
            if self.verbose:
                print(f"rec_mouse # {count}")
            has_quit = keyboard.is_pressed("escape")

            mouse.on_click(partial(add_pos, "left"))
            mouse.on_middle_click(partial(add_pos, "middle"))
            mouse.on_right_click(partial(add_pos, "right"))
            mouse.on_double_click(partial(add_pos, "double"))
            time.sleep(self.delay)

        keyboard.unhook_all()
        mouse.unhook_all()
        if self.verbose:
            print("Positions")
            print(positions)
        self.config.full_config["BUTTONS"][idx]["mouse_movements"] = positions
        self.config.save_config()
    # rec_mouse

    def _get_action_from_pos(self) -> Tuple[str, Any]:
        """Get return and fix comments"""
        # Error if the user hit a button that was bigger than actions, so we can't call anything
        if self.last_pressed_pos > len(self.config.actions.keys()):
            _msg = (
                "Hit a button that's not defined in the config file!"
                f"pos: {self.last_pressed_pos} larger than buttons length"
                "Doing nothing"
            )
            return ("err", _msg)

        _action_matched_key = None
        _action = None

        for idx, action_key in enumerate(self.config.actions.keys(), start=1):
            if idx == self.last_pressed_pos:
                _action_matched_key = action_key
                _action = self.config.actions[action_key]
                break
        return (_action_matched_key, _action)
    # _get_action_from_pos

    def _get_func_from_pos(self) -> Tuple[str, str]:
        """Get function name from position within actions from config.
        Errors will result in returning ("err", msg)
        Returns:
            Tuple[str, str] - (func, value) func is actionmanager.actions's key name, value is the args
        """
        func_name = None
        value = None
        # Error if the user hit a button that was bigger than actions, so we can't call anything
        if self.last_pressed_pos > len(self.config.actions.keys()):
            _msg = (
                "Hit a button that's not defined in the config file!"
                f"pos: {self.last_pressed_pos} larger than buttons length"
                "Doing nothing"
            )
            return ("err", _msg)

        # Get function name + value from actions
        for idx, item in enumerate(self.config.actions.values, start=1):
            if idx == self.last_pressed_pos:
                func_name = item["func"]
                if "extra" in item:
                    extra = item["extra"]
                break
        return (func_name, value)
    # _get_func_from_pos

    def _run_func_from_name(self, func_name: str, extra: str):
        """Run the actual function with or without extra params from func_name
        Params:
            func_name - str, function name that must match a method in FuncManager
            extra - str [None], extra params for func_name
        """

        # Get function from string, this must match!
        # TODO: try/catch? or return err
        try:
            _func = getattr(self.func_manager, func_name)
        except AttributeError:
            # TODO: show messagebox?
            print(f"{func_name} has not been defined in FuncManager!")
            return

        # Call function, with params if extra is defined
        # - 1 since the button pos is not 0 indexed
        if extra is None:
            _func(self.last_pressed_pos - 1)
        else:
            _func(self.last_pressed_pos - 1, extra)
    # _run_func_from_name


# MacroManager

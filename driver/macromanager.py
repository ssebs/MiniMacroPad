#!/usr/bin/env python3
# macromanager.py - Manager for the Macros for use with the MiniMacroPad
import keyboard
import mouse
import time

from enum import Enum
from tkinter import Tk
from typing import Tuple

from config import Config


class Actions(Enum):
    ALT_TAB = 0
    BUTTON_PRESS = 1


class FuncManager():
    """Actually run the functions for the Macro
    TODO: Move to own file
    """

    def __init__(self, config: Config, default_delay: float = 0.2):
        self.config = config
        self.default_delay = default_delay
    # __init__

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

    # # All send_<blah> functions should be exposed to the user somehow, this is what they'll put in the configs # #

    def send_text(self, idx: int):
        keyboard.write(self.config.buttons[idx]["text"])
    # send_text

# FuncManager


class MacroManager():
    """
    Manager for the Macros for use with the MiniMacroPad
    (Instantiates a Config object)
    Params:
        root_win - Tk, root container
        config_path - str [None], path to config, if None use default.
        verbose - bool [False], verbosity
    Methods:
        run_action
    """

    def __init__(self, root_win: Tk, config_path: str = None, verbose: bool = False):
        self.verbose: bool = verbose
        # Load json Config from file, takes config_path if provided
        self.config: Config = Config(config_path=config_path, verbose=verbose)

        self.func_manager: FuncManager = FuncManager(config=self.config)

        # Set root_win from param
        self.root_win: Tk = root_win

        # TODO: replace this comment
        self.last_pressed_pos = -1
        self.delay = 0.02  # seconds

    # __init__

    def run_action(self, action: Actions, position: int = -1):
        """Run an action depending on the action type
        Params:
            action - Actions(Enum), action type to run
            position - int [-1], position where to call the action function from
        """
        print("Running action")
        if action == Actions.ALT_TAB:
            if self.verbose:
                print("Running alt tab")
            self.func_manager.run_alt_tab()
        elif action == Actions.BUTTON_PRESS:
            # TODO: make sure it's not -1
            if self.verbose:
                print("Running button press")
            self.last_pressed_pos = position

            # Get function name from position within buttons[] from config
            func_name, extra = self._get_func_from_pos()
            # Print error if there is one and return
            if func_name is None or func_name == "err":
                print(extra)
                return

            # Actually run the function, must be defined in FuncManager
            # TODO: try/catch
            self._run_func_from_name(func_name, extra)

            print(f"btn press: {position}")
        else:
            print("Must choose from Actions enum in macromanager.py")
    # run_action

    def _get_func_from_pos(self) -> Tuple[str, str]:
        """Get function name from position within buttons[] from config.
        Errors will result in returning ("err", msg)
        Returns:
            Tuple[str, str] - (func_name, extra). Extra is any additional params defined as "extra" in the config.
        """
        func_name = None
        extra = None
        # Error if the user hit a button that was bigger than buttons[], so we can't call anything
        if self.last_pressed_pos > len(self.config.buttons):
            _msg = (
                "Hit a button that's not defined in the config file!"
                f"pos: {self.last_pressed_pos} larger than buttons length"
                "Doing nothing"
            )
            return ("err", _msg)

        # Get function name + extra if it has it from buttons[]
        for idx, item in enumerate(self.config.buttons, start=1):
            if idx == self.last_pressed_pos:
                func_name = item["func"]
                if "extra" in item:
                    extra = item["extra"]
                break
        return (func_name, extra)
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

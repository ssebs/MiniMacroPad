#!/usr/bin/env python3
# macromanager.py - Manager for the Macros for use with the MiniMacroPad
import keyboard
import mouse
import time

from enum import Enum
from tkinter import Tk

from config import Config


class Actions(Enum):
    ALT_TAB = 0
    BUTTON_PRESS = 1


class FuncManager():
    """Actually run the functions for the Macro
    """

    def __init__(self, default_delay: float = 0.2):
        self.default_delay = default_delay
    # __init__

    def run_func(self, func_name: str, params: list):
        pass

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

        self.func_manager: FuncManager = FuncManager()

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
            print(f"btn press: {position}")
        else:
            print("Must choose from Actions enum in macromanager.py")
# MacroManager

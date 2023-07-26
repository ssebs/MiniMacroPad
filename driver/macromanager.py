#!/usr/bin/env python3
# macromanager.py - Manages Macros

from enum import Enum
from tkinter import Tk
from serial import Serial

from config import Config
from macrodisplay import MacroDisplay


class Actions(Enum):
    ALT_TAB = 0
    BUTTON_PRESS = 1


class MacroManager():
    """
    Manager for the Macros for use with the MiniMacroPad.
    Instantiates a Config object
    """

    def __init__(self, root_win: Tk, config_path: str = None, verbose: bool = False):
        self.verbose: bool = verbose
        # Load json Config from file, takes config_path if provided
        self.config: Config = Config(config_path=config_path, verbose=verbose)

        # Set root_win from param
        self.root_win: Tk = root_win
        # Set defaults as None, will be updated later
        self.arduino_conn: Serial = None

        # Initialize the GUI & save to self.macro_display
        self.macro_display: MacroDisplay = self.init_gui()
    # __init__

    def init_gui(self) -> MacroDisplay:
        window = MacroDisplay(
            container=self.root_win, grid_size=self.config.config["SIZE"], buttons=self.config.buttons, macro_manager=self, verbose=self.verbose)

    def run_action(self, action: Actions, position: int = -1):
        print("Running action")
        if action == Actions.ALT_TAB:
            print("alt tab")
        elif action == Actions.BUTTON_PRESS:
            # TODO: make sure it's not -1
            print(f"btn press: {position}")
        else:
            print("Must choose from Actions enum in macromanager.py")

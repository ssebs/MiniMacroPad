#!/usr/bin/env python3
# macromanager.py - Manages Macros

from config import Config
from tkinter import Tk
from serial import Serial


class MacroManager():
    """
    Manager for the Macros for use with the MiniMacroPad.
    Instantiates a Config object
    """
    def __init__(self, root_win: Tk, arduino_conn: Serial = None, config_path: str = None, verbose: bool = False):
        # Load json Config from file
        self.config: Config = Config(config_path=config_path, verbose=verbose)

        self.root_win: Tk = root_win
        self.arduino_conn: Serial = arduino_conn
    # __init__

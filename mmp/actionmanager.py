#!/usr/bin/env python3
# actionmanager.py - Manager for the actions to run. (keyboard & mouse operations)
import keyboard
import mouse
import time

from datetime import datetime
from enum import Enum, auto
from tkinter import Tk
from typing import Tuple, Dict, List

from config import Config
from stringlooper import StringLooper


class ActionManager():
    """
    Manager for the actions to run. (keyboard & mouse operations)
    """

    def __init__(self, config: Config, default_delay: float = 0.2, verbose: bool = False):
        """
        REPLACE_ME
        """
        self.verbose: bool = verbose
        self.config: Config = config
        self.default_delay: float = default_delay
        self.loopers: Dict[StringLooper] = self._parse_loopers()
        self.actions = {
            "DELAY": self.do_delay,
            "KB_SEND_HOTKEY": self.do_kb_send_hotkey,
            "KB_SEND_STR": self.do_kb_send_str,
            # "KB_SEND_LOOP": replace,
            # "KB_KEY_PRESS": replace,
            # "KB_KEY_DOWN": replace,
            # "KB_KEY_UP": replace,
            # "MOUSE_CLICK": replace,
            # "MOUSE_DOWN": replace,
            # "MOUSE_UP": replace,
            # "MOUSE_MOVE_TO": replace,
            # "MOUSE_RECORD": replace,
        }
    # __init__

    # TODO: Implement this!
    # def set_delay(func):
    #     """wrapper function that sets the default delay if none has been set"""
    #     def outware(*args):
    #         self = args[0]
    #         _delay = delay if delay else self.default_delay
    #         func(*args)
    #     return outware

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

    def _press_and_hold(self, keys: List[str], delay: float = None):
        """Takes a list of keys to hold at the same time
        Params:
            keys - List[str], list of keys to hold simultaneously
            delay - float, how long in seconds to hold the keys down. Default to self.default_delay
        """
        # TODO: Make this a wrapper func
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
            # Ignore if sending a string
            if not key.startswith("TXT="):
                keyboard.release(key)
    # _press_and_hold

    def do_delay(self, delay: float = None):
        """Run time.sleep for delay, or default delay"""
        _delay = delay if delay else self.default_delay
        time.sleep(_delay)
    # do_delay

    def do_kb_send_hotkey(self, hotkey: List[str], delay: float = None):
        """Takes a list of keys and holds at the same time
        Params:
            keys - List[str], list of keys to hold simultaneously
            delay - float, how long in seconds to hold the keys down. Default to self.default_delay
        """
        # TODO: Make this a wrapper func
        _delay = delay if delay else self.default_delay

        # Press all keys down
        for key in keys:
            keyboard.press(key)

        # Wait

        time.sleep(_delay)
        # Release all keys
        for key in keys:
            keyboard.release(key)
    # do_kb_send_hotkey

    def do_kb_send_str(self, string_to_send: str):
        """Write string_to_send using the keyboard
        Params:
            string_to_send - str, The string to write with the keyboard
        """
        _delay = delay if delay else self.default_delay
        keyboard.write(string_to_send, delay)
#!/usr/bin/env python3
# actionmanager.py - Manager for the actions to run. (keyboard & mouse operations)
import keyboard
import mouse
import time

from datetime import datetime
from enum import Enum, auto
from tkinter import Tk
from typing import Tuple, Dict, List

from mmp.config import Config
from mmp.stringlooper import StringLooper


class ActionManager():
    """
    Manager for the actions to run. (keyboard & mouse operations)
    """
    LOOPER_ACTIONS: List[str] = [
        "KB_SEND_LOOP_UP",
        "KB_SEND_LOOP_DOWN",
        "KB_SEND_LOOP_RAND"
    ]

    def __init__(self, config: Config, default_delay: float = 0.2, verbose: bool = False):
        """
        REPLACE_ME
        """
        self.verbose: bool = verbose
        self.config: Config = config
        self.default_delay: float = default_delay
        self.loopers: Dict[StringLooper] = self._parse_loopers()

        # ACTION_NAME:function mapping
        self.actions = {
            "DELAY": self.do_delay,
            "KB_SEND_HOTKEY": self.do_kb_send_hotkey,
            "KB_SEND_STR": self.do_kb_send_str,
            "KB_SEND_LOOP_UP": self.do_kb_loop_up,
            "KB_KEY_PRESS": self.do_kb_key_press,
            "KB_KEY_DOWN": self.do_kb_key_down,
            "KB_KEY_UP": self.do_kb_key_up,
            # "MOUSE_CLICK": replace,
            # "MOUSE_DOWN": replace,
            # "MOUSE_UP": replace,
            # "MOUSE_MOVE_TO": replace,
            # "MOUSE_RECORD": replace,
        }
    # __init__

    # TODO: Create another wrapper for logging actions
    def set_delay(func):
        """wrapper function that sets the default delay if none has been set"""
        def outware(*args, **kwargs):
            self = args[0]
            _arg_delay = None
            # Set the default delay if the func param doesn't use it
            if "delay" in kwargs:
                _arg_delay = kwargs["delay"]
            _delay = _arg_delay if _arg_delay else self.default_delay
            func(*args)  # TODO: FIX pass delay to the func
        return outware

    def _parse_loopers(self) -> dict:
        """parse config json to create string loopers
        (Instantiates StringLooper objects)
        Returns:
            dict[str, StringLooper]
        """
        # TODO: fix the exception handling! make it return an error instead of raising here
        _looper = {}
        # TODO: redocument / cleanup

        # Go thru all actions, find the ones with loopers, and instantiate StringLoopers from that
        for _action_name, _action_item in self.config.actions.items():
            # For the actual action within the _action_item list
            for _action in _action_item:
                func_name, func_value = next(iter(_action.items()))
                if func_name in ActionManager.LOOPER_ACTIONS:
                    # Found a looper!

                    # Check func_value, make sure that exists within config.DATA
                    if func_value not in self.config.data.keys():
                        raise Exception(f"Failed to find {func_value} in {self.config.data}")

                    _looper[func_value] = StringLooper(self.config.data[func_value])

        if self.verbose:
            print("loopers:")
            for looper in _looper.values():
                print(looper)

        # Return new dict
        return _looper
    # _parse_loopers

    def do_kb_loop_up(self, data_name: List[str]):
        """TODO: document"""
        self.loopers[data_name].loop_up()
        if self.verbose:
            print(
                f"loop_up: {self.loopers[data_name].get_str()}, list: {data_name}")
        keyboard.write(self.loopers[data_name].get_str())
    # do_kb_loop_up

    def _press_and_hold(self, keys: List[str], delay: float = None):
        """Takes a list of keys to hold at the same time
        Params:
            keys - List[str], list of keys to hold simultaneously
            delay - float, how long in seconds to hold the keys down. Default to self.default_delay
        """
        # Press all keys down
        for key in keys:
            # If we are sending a string, use write instead
            if key.startswith("TXT="):
                keyboard.write(key[4:])
                time.sleep(delay)
            else:
                keyboard.press(key)
        # Wait
        time.sleep(delay)
        # Release all keys
        for key in keys:
            # Ignore if sending a string
            if not key.startswith("TXT="):
                keyboard.release(key)
    # _press_and_hold

    @set_delay
    def do_delay(self, delay: float = None):
        """Run time.sleep for delay, or default delay"""
        time.sleep(delay)
    # do_delay

    @set_delay
    def do_kb_send_hotkey(self, hotkey: List[str], delay: float = 0.2):
        """Takes a list of keys and holds at the same time
        Params:
            keys - List[str], list of keys to hold simultaneously
            delay - float, how long in seconds to hold the keys down. Default to 0.2s
        """
        # Press all keys down
        for key in hotkey:
            keyboard.press(key)

        # Wait
        if delay:
            time.sleep(delay)

        # Release all keys
        for key in hotkey:
            keyboard.release(key)
    # do_kb_send_hotkey

    @set_delay
    def do_kb_send_str(self, string_to_send: str, delay: float = None):
        """Write string_to_send using the keyboard
        Params:
            string_to_send - str, The string to write with the keyboard
        """
        keyboard.write(string_to_send, delay)
    # do_kb_send_str

    def do_kb_key_press(self, key_to_press: str):
        """Press and release a keyboard button
        Params:
            key_to_press - str, The keyboard button to press and release
        """
        keyboard.press_and_release(key_to_press)
    # do_kb_key_press

    def do_kb_key_down(self, key_to_press: str):
        """Press down a keyboard button
        Params:
            key_to_press - str, The keyboard button to press
        """
        keyboard.press(key_to_press)
    # do_kb_key_down

    def do_kb_key_up(self, key_to_release: str):
        """Release a keyboard button
        Params:
            key_to_release - str, The keyboard button to release
        """
        keyboard.release(key_to_release)
    # do_kb_key_up

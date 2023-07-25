#!/usr/bin/env python3
# util.py - Util stuff
from tkinter import *
import tkinter.messagebox as msgbox
import sys
import json
import random
import time
import os.path
import keyboard
import mouse
import serial.tools.list_ports
from typing import Tuple, List
from functools import partial

from enum import Enum


class Config():
    """Config class
    Handles config files + loading up the json.
    Config is accessible via <configObject>.config["KEY"]
    """

    def __init__(self, config_path: str = None, verbose: bool = False):
        self.verbose = verbose
        self.default_config_path = "./driver/res/sampleconfig.json"

        # If config_path is defined, use it otherwise use default path
        self.default_path = os.path.expanduser(
            "~") + "/minimacropad-config.json"
        self.path = config_path if config_path else self.default_path

        # Load JSON config from path, write default if nothing is found
        self.full_config = self.load_config()

        # Shortcuts for accessing
        self.config = self.full_config["CONFIG"]
        self.buttons = self.full_config["BUTTONS"]
        self.data = self.full_config["DATA"]

        self.serial = self.config["SERIAL"]
    # init

    def load_config(self) -> dict:
        """Loads JSON config from self.path"""
        try:
            with open(self.path, "r") as f:
                try:
                    return json.loads(f.read())
                except Exception as e:
                    msg = f"Failed to parse JSON from {self.path} config file."
                    print(msg)
                    raise e
        except FileNotFoundError:
            if self.default_path == self.path:
                self.save_default_config()
                return self.load_config()
            else:
                msg = f"Failed to find {self.path} config file. Remove this param or create the file"
                print(msg)
                raise Exception(msg)
        except Exception as e:
            print(f"Failed to load {self.path} config file.")
            raise e
    # load_config

    def save_default_config(self):
        """Saves sampleconfig.json to default directory"""
        _config = None
        try:
            with open(self.default_config_path, "r") as f:
                _config = f.read()
        except FileNotFoundError:
            msg = f"Failed to find {self.default_config_path}"
            print(msg)
            raise Exception(msg)
        except Exception as e:
            print("Failed to load config file")
            print(e)
            raise e
        try:
            with open(self.path, "w") as f:
                f.write(_config)
        except Exception as e:
            print("Failed to save config file")
            print(e)
            raise e
    # save_default_config

    def get_path(self):
        return self.path
    # get_path

# Config class


class Util():
    # TODO: Rename this, this is the worst possible name for this kind of thing
    # i mean, it's not even static or anything
    # devs pls
    def __init__(self, config: Config, verbose=False):
        self.verbose = verbose
        self.config = config
        self.pos = -1
        self.delay = 0.02  # seconds
        self.loopers = self.parse_loopers()
    # init

    def parse_loopers(self) -> dict:
        """parse json to create string loopers"""
        _looper = {}
        for btn in self.config.buttons:
            if "extra" in btn:
                try:
                    # If the string array name is not in data
                    if btn["extra"] not in self.config.data:
                        raise Exception(
                            f"Failed to find {btn['extra']} in {self.config.data}")
                    # Get string array from extra variable
                    tmp_loop = StringLooper(
                        self.config.data[btn['extra']], btn['extra']
                    )
                    # Add to dict
                    _looper[btn['extra']] = tmp_loop

                except Exception as e:
                    print("Failed to add looper")
                    raise e

        if self.verbose:
            print("loopers:")
            for looper in _looper.values():
                looper.print_str()

        # Return new dict
        return _looper
    # parse_loopers

    def handle_btn_press(self, position: int):
        """Calls function defined in position in BUTTONS"""
        if self.verbose:
            print(f"Pressed: {position}")
        self.pos = position

        if position > len(self.config.buttons):
            print("Hit a button that's not defined in the config file!")
            print(f"pos: {position} larger than buttons length")
            print("Doing nothing")
            return

        # Get function name and extra from button position
        func_name = None
        extra = None
        for idx, item in enumerate(self.config.buttons, start=1):
            if idx == position:
                func_name = item["func"]
                if "extra" in item:
                    extra = item["extra"]
                break
        if func_name is None:
            raise Exception(f"Unable to find function in pos {position}.")

        # Get func name from string
        func = getattr(self, func_name)
        # Call function, with params if extra is defined
        # - 1 since the button pos is not 0 indexed
        if extra is None:
            func(position - 1)
        else:
            func(position - 1, extra)
    # handle_btn_press

    def press_hold(self, keys: list):
        """Takes a list of keys to hold at the same time"""
        # Press all keys down
        for key in keys:
            # If we are sending a string, use write instead
            if key.startswith("TXT="):
                keyboard.write(key[4:])
                time.sleep(self.delay)
            else:
                keyboard.press(key)
        # Wait
        time.sleep(self.delay)
        # Release all keys
        for key in keys:
            # Ignore releasing strings
            if not key.startswith("TXT="):
                keyboard.release(key)
    # press_hold

    # Macro Functions below
    def outware(func):
        def prepost(*args):
            self = args[0]

            if "pre" in self.config.buttons[self.pos - 1]:
                for keys in self.config.buttons[self.pos - 1]["pre"]:
                    self.press_hold(keys)
            func(*args)
            if "post" in self.config.buttons[self.pos - 1]:
                for keys in self.config.buttons[self.pos - 1]["post"]:
                    self.press_hold(keys)
        return prepost
    # wrapper func to handle pre/post hotkeys

    def alt_tab(self):
        """press alt tab for use when clicking on a macro button"""
        self.press_hold(["alt", "tab"])
        time.sleep(self.delay * 2)
    # alt_tab

    # # User Macro Functions # #

    # no outerwear since send_mouse uses it
    def rec_mouse(self, idx: int):
        """Record mouse inputs"""
        positions = []
        has_quit = False
        count = 0

        print("0")
        # mouse.wait(button='left', target_types='up')  # wait for first click
        # print(1)

        def add_pos():
            positions.append(mouse.get_position())
            # custom diag box
            # msgbox.askquestion(title="Set Mouse Macro", message="Would you like that to be a left, right, or double click?", )

        def leave():
            has_quit = True

        while not has_quit and count < 999999999:
            count += 1
            print(f"not has quit # {count}")
            has_quit = keyboard.is_pressed("escape")
            mouse.on_middle_click(add_pos)
            # mouse.on_right_click(lambda: has_quit=True)
            time.sleep(self.delay)

        # when recording, have user click to start, then move to correct pos, then right click to save, double to exit. if not double then repeat process
        # click btn > move to pos > right click (save pos to list) > double click (to loop to beginning)

        keyboard.unhook_all()
        mouse.unhook_all()
        print(remove_duplicates(positions))
    # rec_mouse

    @outware
    def send_text(self, idx: int):
        keyboard.write(self.config.buttons[idx]["text"])
    # send_text func from json

    @outware
    def send_hotkey(self, idx: int):
        if "hotkeys" not in self.config.buttons[idx]:
            raise Exception(f"Hotkeys not defined in BUTTONS[{idx}]")

        for keys in self.config.buttons[idx]["hotkeys"]:
            self.press_hold(keys)
    # send_hotkey func from json

    @outware
    def send_mouse(self, idx: int):
        pass
    # send_mouse func from json

    @outware
    def loop_up(self, idx: int, extra: str):
        self.loopers[extra].loop_up()
        keyboard.write(self.loopers[extra].get_str())
    # loop_up func from json

    @outware
    def loop_down(self, idx: int, extra: str):
        self.loopers[extra].loop_down()
        keyboard.write(self.loopers[extra].get_str())
    # loop_down func from json

    @outware
    def loop_rand(self, idx: int, extra: str):
        self.loopers[extra].loop_rand()
        keyboard.write(self.loopers[extra].get_str())
    # loop_rand func from json


class StringLooper():
    def __init__(self, strings: list, name: str):
        self.strings = strings
        self.name = name
        self.max = len(strings) - 1
        self.min = 0
        self.pos = 0

    def get_str(self):
        return self.strings[self.pos]

    def loop_up(self):
        if self.pos >= self.max:
            self.pos = 0
            return
        self.pos += 1

    def loop_down(self):
        if self.pos <= 0:
            self.pos = self.max
            return
        self.pos -= 1

    def loop_rand(self):
        self.pos = random.randint(self.min, self.max)

    def print_str(self):
        print(f"  {self.name} - pos: {self.pos}, min: {self.min}, max: {self.max}")


# Exceptions
class CustomSerialException(Exception):
    pass


class SerialNotFoundException(CustomSerialException):
    pass


class SerialMountException(CustomSerialException):
    pass

# Helper functions


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)) + "\\res")
    return os.path.join(base_path, relative_path)


def get_serial_port_name(name: str, is_COM_name: bool = True, verbose: bool = False) -> str:
    """
    Gets the COM port as a str that the arduino is connected to
    params:
        name - name of what you want to match (e.g. COM1)
        is_COM_name - is this a COM name or description? (e.g. COM1 vs USB Serial Device (COM1))
    Returns:
        Serial COM port as str
    """
    ports = list(serial.tools.list_ports.comports())
    if verbose:
        print("Serial Ports:")
    for p in ports:
        if verbose:
            print(f"  {p.name} - {p.description}")
        if is_COM_name:
            if p.name == name:
                return p.name
        else:
            if name in p.description:
                return p.name
    return None
# end load_port


def remove_duplicates(lst: List[Tuple[int, int]]):
    # Create an empty dictionary to store tuples as keys
    encountered = {}
    # Create an empty list to store unique tuples
    result = []
    # Iterate through the input list
    for tup in lst:
        # If the tuple has not been encountered before,
        # add it to the dictionary and the result list
        if tup not in encountered:
            encountered[tup] = True
            result.append(tup)
    # Return the list of unique tuples
    return result

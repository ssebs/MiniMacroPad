#!/usr/bin/env python3
# util.py - Util stuff
import json
from enum import Enum
import random
from tkinter import ttk
import pyautogui
import os.path 

class Config():
    DEFAULT_CONFIG = {
        "CONFIG": {
            "SIZE": {"x": 3, "y": 3},
            "MONITOR": 1,
            "SERIAL": {
                "QUERY": "USB Serial Device",
                "BAUDRATE": 9600,
                "TIMEOUT":  0.1
            }
        },
        "DATA": {},
        "BUTTONS": [
            {
                "pos": 1,
                "text": "Test\n",
                "func": "send_text"
            },
        ]
    }

    def __init__(self, config_path: str = None, verbose: bool = False):
        self.verbose = verbose
        self.default_path = os.path.expanduser("~") + "/minimacropad-config.json"
        self.path = config_path if config_path else self.default_path
        
        self.config = self.load_config()["CONFIG"]
        self.size = self.config["SIZE"]
        self.monitor = self.config["MONITOR"]
        self.serial = self.config["SERIAL"]
    # init

    def load_config(self) -> dict:
        try:
            with open(self.path, "r") as f:
                try:
                    return json.loads(f.read())
                except Exception as e:
                    print(f"Failed to parse JSON from {path} config file.")
        except FileNotFoundError:
            self.save_default_config()
            self.load_config()
        except Exception as e:
            print(f"Failed to load {path} config file.")
            raise e
    # load_config

    def save_default_config(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(self.DEFAULT_CONFIG))
    # save_default_config

    def get_path(self):
        return self.path

class Util():
    def __init__(self, config_path: str, verbose=False):
        self.verbose = verbose
        self.loopers = {}

        self.config = self.load_config(config_path)
        self.buttons = self.config["BUTTONS"]

        self.parse_config()
    # init

    def load_config(self, path: str) -> dict:
        try:
            with open(path, "r") as f:
                try:
                    return json.loads(f.read())
                except Exception as e:
                    print(f"Failed to parse JSON from {path} config file.")
        except Exception as e:
            print(f"Failed to load {path} config file.")
            raise e
    # load_config

    def parse_config(self):
        for btn in self.buttons:
            if "extra" in btn:
                try:
                    # If the string array name is not in data
                    if btn["extra"] not in self.config["DATA"]:
                        raise Exception(
                            f"Failed to find {btn['extra']} in {self.config['DATA']}")
                    # Get string array from extra variable
                    tmp_loop = StringLooper(
                        self.config["DATA"][btn['extra']], btn['extra']
                    )
                    self.loopers[btn['extra']] = tmp_loop
                except Exception as e:
                    print("Failed to add looper")
                    raise e
        if self.verbose:
            print("loopers")
            for l in self.loopers.values():
                l.print_str()
        # self.loopers.print_str()

    def handle_btn_press(self, position: int):
        print(f"Pressed: {position}")

        if position > len(self.buttons):
            print("Hit a button that's not defined in the config file!")
            print(f"pos: {position} larger than buttons length")
            print("Doing nothing")
            return
        
        func_name = None
        extra = None
        for item in self.buttons:
            if item['pos'] == position:
                func_name = item["func"]
                if "extra" in item:
                    extra = item["extra"]
        if func_name is None:
            raise Exception(f"Unable to find function in pos {position}.")

        # Get func name from string
        func = getattr(self, func_name)
        if extra is None:
            func(position - 1)
        else:
            func(position - 1, extra)

    # Functions below
    def send_text(self, idx: int):
        pyautogui.write(self.buttons[idx]["text"])

    def send_undo(self, idx: int):
        pyautogui.hotkey('ctrl', 'z')

    def send_hotkey(self, idx: int):
        if "hotkeys" not in self.buttons[idx]:
            raise Exception(f"Hotkeys not defined in BUTTONS[{idx}]")

        for keys in self.buttons[idx]["hotkeys"]:
            pyautogui.hotkey(*keys)

    def loop_up(self, idx: int, extra: str):
        self.loopers[extra].loop_up()
        self._pre(idx)
        pyautogui.write(self.loopers[extra].get_str())
        self._post(idx)
    # loop_up func from json

    def loop_down(self, idx: int, extra: str):
        self.loopers[extra].loop_down()
        self._pre(idx)
        pyautogui.write(self.loopers[extra].get_str())
        self._post(idx)
    # loop_down func from json

    def loop_rand(self, idx: int, extra: str):
        self.loopers[extra].loop_rand()
        self._pre(idx)
        pyautogui.write(self.loopers[extra].get_str())
        self._post(idx)
    # loop_rand func from json

    def _pre(self, idx: int):
        """Handle pre commands"""
        if "pre" in self.buttons[idx]:
            for keys in self.buttons[idx]["pre"]:
                pyautogui.hotkey(*keys)
    # _pre

    def _post(self, idx: int):
        """Handle post commands"""
        if "post" in self.buttons[idx]:
            for keys in self.buttons[idx]["post"]:
                pyautogui.hotkey(*keys)
    # _post


class StringLooper():
    def __init__(self, strings: list, name: str):
        self.strings = strings
        self.name = name
        self.max = len(strings)
        self.min = 0
        self.pos = 0

    def get_str(self):
        return self.strings[self.pos]

    def loop_up(self):
        if self.pos == self.max:
            self.pos = 0
        self.pos += 1

    def loop_down(self):
        if self.pos == 0:
            self.pos == self.max
        self.pos -= 1

    def loop_rand(self):
        self.pos = random.randint(self.min, self.max)

    def print_str(self):
        print(f"{self.name} - pos: {self.pos}, min: {self.min}, max: {self.max}")


# Exceptions
class CustomSerialException(Exception):
    pass


class SerialNotFoundException(CustomSerialException):
    pass


class SerialMountException(CustomSerialException):
    pass

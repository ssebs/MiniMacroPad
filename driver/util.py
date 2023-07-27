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
from datetime import datetime
import serial.tools.list_ports
from typing import Tuple, List, Dict
from functools import partial

from enum import Enum
from config import Config


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


# Helper (util) functions
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)) + "\\res")
    return os.path.join(base_path, relative_path)


def get_serial_port_name(name: str, is_COM_name: bool = True, verbose: bool = False) -> str:
    """
    Gets the COM port as a str that the arduino is connected to
    Params:
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

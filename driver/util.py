#!/usr/bin/env python3
# util.py - Util stuff
import os.path
import serial.tools.list_ports
import sys

from tkinter import *

# # Constants # #
DEBUG = False
ICON_PATH = 'bell.ico'
SFX_PATH = 'snap.mp3'
# SERIAL_QRY = "Arduino Leonardo"
# SERIAL_QRY = "USB Serial Device (COM7)"
# SERIAL_BAUD = 9600
# SERIAL_TIMEOUT = 0.1
MSGBOX_TITLE = "MiniMacroPad - Serial Exception"


# Exceptions


class CustomSerialException(Exception):
    pass


class SerialNotFoundException(CustomSerialException):
    pass


class SerialMountException(CustomSerialException):
    pass


# Helper (util) functions
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)) + "\\res")
    return os.path.join(base_path, relative_path)
# resource_path


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
# get_serial_port_name

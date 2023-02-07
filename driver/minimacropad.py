#!/usr/bin/env python3
# minimacropad.py - A python driver to provide functionality to the mini macro pad.

import os
import sys
import time
import signal
import threading

import serial
import serial.tools.list_ports

import ttkbootstrap as ttk
from tkinter import Tk, messagebox
from ttkbootstrap.constants import *
from playsound import playsound

from macrodisplay import MacroDisplay
from util import (
    Util, Config, CustomSerialException,
    SerialNotFoundException, SerialMountException,
    resource_path
)

DEBUG = False
RETRY_COUNT = 5
ICON_PATH = 'bell.ico'
SFX_PATH = 'snap.mp3'
# SERIAL_QRY = "Arduino Leonardo"
SERIAL_QRY = "USB Serial Device (COM7)"
SERIAL_BAUD = 9600
SERIAL_TIMEOUT = 0.1
MSGBOX_TITLE = "MiniMacroPad - Serial Exception"


def main():
    """
    Main function
    TODO: Make this OOP instead of using global vars and constants
    """
    if DEBUG:
        print("Driver for macro pad:")

    # Load json Config
    config = Config(verbose=DEBUG)

    # Load arduino serial connection
    for tries in range(RETRY_COUNT):
        try:
            arduino = init_arduino(config)
            # macro_display = init_gui()  # sets global root, returns MacroDisplay
        except serial.SerialException as e:
            print(e)
            messagebox.showerror(title=MSGBOX_TITLE,
                                 message=f"{str(e)}\n\nCheck if you have another instance open?")
            sys.exit(0)
        except CustomSerialException as e:
            print(e)
            do_try_again = messagebox.askyesno(title=MSGBOX_TITLE,
                                               message=f"{str(e)}\n\nWant to try loading again?")
            if do_try_again:
                continue
            else:
                sys.exit(0)
            sys.exit(0)
        except Exception as e:
            print(e)
            raise e
            sys.exit(1)
        # break if trying succeeds
        break

    # Setup Util class
    util = Util(config.get_path(), verbose=DEBUG)

    window = init_gui(util, config)

    # Setup Serial comm thread
    global thread1
    # For the close icon in the GUI, stop the thread too
    global do_close
    do_close = False

    thread1 = threading.Thread(target=main_loop, args=(
        arduino, root, window, util), daemon=True)
    thread1.start()

    root.mainloop()
# end main


def init_arduino(config: Config) -> serial.Serial:
    """
    Initialize serial COM port and return it. Uses SERIAL_QRY to find the port
    Returns:
        Serial object of arduino / teensy
    """
    # what my PC says the teensy LC is called, could use COM7 but that could change
    signal.signal(signal.SIGINT, signal.default_int_handler)
    serial_port = load_port(
        name=config.serial["QUERY"], is_COM_name=False, verbose=DEBUG)

    if serial_port is None:
        raise SerialNotFoundException(
            f"Failed to load serial port: {config.serial['QUERY']}")

    arduino = serial.Serial(port=serial_port, baudrate=config.serial["BAUDRATE"],
                            timeout=config.serial["TIMEOUT"])
    if arduino is None:
        raise SerialMountException(
            f"Failed to mount Serial port: {config.serial['QUERY']}")

    return arduino
# end init_arduino


def init_gui(util: Util, config: Config) -> MacroDisplay:
    """
    Initialize the gui, uses global root var.
    Returns:
        MacroDisplay object for GUI
    """
    global root
    root = ttk.Window(themename="darkly")
    macro_display = MacroDisplay(
        root, grid_size=config.size, macro_items=util.buttons, util=util, verbose=DEBUG)

    root.protocol("WM_DELETE_WINDOW", handle_close)
    root.iconbitmap(resource_path(ICON_PATH))
    # root.resizable(False, False)
    root.title("MiniMacroPad")

    posX = None
    posY = None
    # Set window location + size
    if config.config["MONITOR"] == -1:
        # dev mode
        posX = root.winfo_screenwidth() + 200
        posY = int(root.winfo_screenheight() / 2) - 200
    elif config.config["MONITOR"] != 1:
        # 2nd monitor
        posX = root.winfo_screenwidth() + int(root.winfo_screenwidth() / 2)
        posY = root.winfo_screenheight() - int(root.winfo_screenheight() / 2)
    else:
        # 1st monitor
        posX = int(root.winfo_screenwidth() / 2)
        posY = int(root.winfo_screenheight() / 2)
    root.geometry(f"{config.config['GUI_SIZE']}+{posX}+{posY}")
    return macro_display
# end init_gui


def main_loop(arduino, root, window, util: Util):
    """
    Handles serial comms
    """
    while True:
        data = str(arduino.readline().decode().strip())
        if data != "":
            if DEBUG:
                print(data)
            if "log:" in data:
                if DEBUG:
                    print(data)

            if ":" not in data:
                # Do something based on button that was pressed
                btn_pos = int(data)
                if btn_pos > len(util.buttons):
                    # 11 => 1
                    if len(str(btn_pos)) > 1:
                        btn_pos = int(str(btn_pos)[-1])
                util.handle_btn_press(btn_pos)
                # Util.MACRO_ITEMS[btn_pos]["func"](btn_pos)
                window.click(btn_pos)

    # end loop
# end main_loop


def load_port(name: str, is_COM_name: bool = True, verbose: bool = False) -> str:
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


def handle_close():
    """
    Handles the close button operation, cleanup stuff
    """
    if thread1 is not None:
        do_close = True
        root.destroy()
        sys.exit(0)
    else:
        print("thread is none")
        root.destroy()
        sys.exit(0)
    # stop thread1
# end handle_close


if __name__ == "__main__":
    main()

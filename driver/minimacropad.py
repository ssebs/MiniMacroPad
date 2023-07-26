#!/usr/bin/env python3
# minimacropad.py - A python driver to provide functionality to the mini macro pad.

import os
import sys
import time
import signal
import threading

from serial import Serial

import ttkbootstrap as ttk
from tkinter import Tk, messagebox
from ttkbootstrap.constants import *
from playsound import playsound

from macrodisplay import MacroDisplay
from util import (
    Util, CustomSerialException,
    SerialNotFoundException, SerialMountException,
    resource_path, get_serial_port_name
)
from config import Config
from macromanager import MacroManager

# TODO: Move these to Util
DEBUG = False
ICON_PATH = 'bell.ico'
SFX_PATH = 'snap.mp3'
# SERIAL_QRY = "Arduino Leonardo"
# SERIAL_QRY = "USB Serial Device (COM7)"
# SERIAL_BAUD = 9600
# SERIAL_TIMEOUT = 0.1
MSGBOX_TITLE = "MiniMacroPad - Serial Exception"


def main():
    """
    Main function
    TODO: Cleanup
    """
    if DEBUG:
        print("Driver for macro pad:")
    # # Globals # #
    # Setup Serial comm thread
    global thread1
    # For the close icon in the GUI, stop the thread too
    global do_close
    do_close = False
    # root for the Tk window
    global root

    # # Actual init stuff # #

    # Setup TK window
    root = ttk.Window(themename="darkly")
    # Setup main macro manager
    macro_manager = MacroManager(root_win=root, verbose=DEBUG)

    # Load arduino
    arduino = init_arduino(macro_manager.config)

    # Setup Util class - rename this
    util = Util(macro_manager.config, verbose=DEBUG)
    window = init_gui(macro_manager)

    # Handle reading serial data via main_loop
    thread1 = threading.Thread(target=main_loop, args=(
        arduino, root, window, util), daemon=True)
    thread1.start()

    # Start GUI thread
    root.mainloop()
# end main


def init_arduino(config: Config) -> Serial:
    """
    Initialize serial COM port and return it. Uses SERIAL_QRY to find the port. Show MsgBox if there's an exception.
    Returns:
        Serial object of arduino / teensy
    """
    # Load arduino serial connection
    for tries in range(config.config["RETRY_COUNT"]):
        # Start stuff we hope to do, raise exceptions if there's an issue
        try:
            # Get serial port name, if available
            serial_port = get_serial_port_name(
                name=config.serial["QUERY"], is_COM_name=False, verbose=DEBUG
            )
            if serial_port is None:
                raise SerialNotFoundException(
                    f"Failed to load serial port: {config.serial['QUERY']}")

            # Get serial connection if we can
            arduino = Serial(port=serial_port, baudrate=config.serial["BAUDRATE"],
                             timeout=config.serial["TIMEOUT"])
            if arduino is None:
                raise SerialMountException(
                    f"Failed to mount Serial port: {config.serial['QUERY']}")
        # end stuff that we hope to do, handle the above exceptions w/ an error msg
        except serial.SerialException as e:
            print(e)
            _msg = f"{str(e)}\n\nCheck if you have another instance open?"
            messagebox.showerror(title=MSGBOX_TITLE, message=_msg)
            sys.exit(0)
        except CustomSerialException as e:
            print(e)
            _msg = f"{str(e)}\n\nWant to try loading again?"
            if messagebox.askyesno(title=MSGBOX_TITLE, message=_msg):
                continue
            else:
                _msg = f"{str(e)}\n\nWant to run in GUI only mode?"
                if messagebox.askyesno(title=MSGBOX_TITLE, message=_msg):
                    return None
                sys.exit(0)
            sys.exit(0)
        except Exception as e:
            print(e)
            raise e
            sys.exit(1)
        # break the loop if loading succeeds
        break
    return arduino
# end init_arduino


def init_gui(util: Util, config: Config) -> MacroDisplay:
    """
    Initialize the gui, uses global root var.
    Returns:
        MacroDisplay object for GUI
    """
    root = ttk.Window(themename="darkly")
    macro_display = MacroDisplay(
        root, grid_size=config.config["SIZE"], buttons=config.buttons, util=util, verbose=DEBUG)

    signal.signal(signal.SIGINT, signal.default_int_handler)
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
    if arduino is None:
        # GUI only mode
        return
    while True:
        try:
            data = str(arduino.readline().decode().strip())
            if data != "":
                if DEBUG:
                    print(data)
                if "log:" in data:
                    if DEBUG:
                        print(data)
                if ":" not in data:
                    # Get button position from data
                    # Button position is NOT 0 indexed!
                    btn_pos = int(data)
                    if btn_pos > len(util.config.buttons):
                        # 11 => 1
                        if len(str(btn_pos)) > 1:
                            btn_pos = int(str(btn_pos)[-1])

                    # Do something based on button that was pressed
                    util.handle_btn_press(btn_pos)
                    window.display_click(btn_pos)  # display on gui
                # end if we got clean data
        except serial.serialutil.SerialException as e:
            print("Device disconnected?")
            print(e)
            handle_close()
            return

    # end loop
# end main_loop


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

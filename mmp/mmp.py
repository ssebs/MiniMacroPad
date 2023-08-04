#!/usr/bin/env python3
# minimacropad.py - A python driver to provide functionality to the mini macro pad.
import sys
import signal
import threading

from serial import Serial
import serial

from functools import partial
import ttkbootstrap as ttk
from tkinter import Tk, messagebox
from ttkbootstrap.constants import *
from typing import Optional

from util import (
    CustomSerialException,
    SerialNotFoundException, SerialMountException,
    resource_path, get_serial_port_name, ICON_PATH, SFX_PATH, MSGBOX_TITLE
)
from config import Config
from macrodisplay import MacroDisplay
from guimanager import GUIManager
from macromanager import MacroManager


def main(is_gui_only: bool, monitor_num: Optional[int], is_verbose: bool):
    """Start initializing the MiniMacroPad & set things up.
    Params:
        is_gui_only - bool, Run in GUI only mode. (Disable serial comms)
        monitor_num - Optional[int], Which monitor to show the GUI on. If None, use what's in the config
        is_verbose - bool, Enable verbosity
    """
    if is_verbose:
        print("Driver for macro pad:")

    # # Globals # #
    # TODO: Stop using globals
    # Setup Serial communication thread
    global thread1
    # Used when clicking the close icon in the GUI, stop the thread too
    global do_close
    do_close = False

    # Create root TK window
    _root: Tk = ttk.Window(themename="darkly")

    # Setup manager that handles actual functionality
    macro_manager: MacroManager = MacroManager(
        root_win=_root, verbose=is_verbose)

    # Load arduino's Serial port if possible
    arduino: Serial = None
    if not is_gui_only:
        if is_verbose:
            print("Loading Serial connection")
        arduino: Serial = init_arduino(macro_manager.config)

    # Setup GUI
    guimanager = GUIManager(macro_manager=macro_manager, cli_arg_monitor_num=monitor_num)

    # Handle reading serial data via arduino_listen_loop
    thread1 = threading.Thread(target=arduino_listen_loop, args=(
        arduino, macro_manager, guimanager.macro_display), daemon=True)
    # TODO: add keyword args to above
    thread1.start()

    # Start GUI thread
    macro_manager.root_win.mainloop()
# end main


def init_arduino(config: Config) -> Serial:
    """
    Initialize serial COM port and return it. Uses SERIAL_QRY to find the port. Show MsgBox if there's an exception.
    Params:
        config - Config object that has relevant info for the RETRY_COUNT, BAUDRATE, etc.
    Returns:
        Serial object of arduino / teensy
    """
    # Load arduino serial connection
    for tries in range(config.config["RETRY_COUNT"]):
        # Start stuff we hope to do, raise exceptions if there's an issue
        try:
            # Get serial port name, if available
            # TODO: Support args here
            serial_port = get_serial_port_name(
                name=config.serial["QUERY"], is_COM_name=False, verbose=config.verbose
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


def arduino_listen_loop(arduino: Serial, macro_manager: MacroManager, window: Tk):
    """
    Handles serial comms & run actions if the arduino sends the right signal
    Params:
        arduino - Serial, the arduino's serial connection. If None then return (leave), else listen for button presses
        macro_manager - MacroManager, instance of the MacroManager class that's used elsewhere in the program
        window - Tk, used to display a button press based on btn_pos
    """
    # GUI only mode
    if arduino is None:
        return

    while True:
        try:
            data = str(arduino.readline().decode().strip())
            if data == "":
                continue
            if macro_manager.verbose:
                print(data)
            if "log:" in data:
                print(data[4:])
            if ":" not in data:
                # Get button position from data

                # NOTE: button position is NOT 0 indexed!
                btn_pos = get_btn_pos(data, macro_manager)
                # Run action
                macro_manager.run_action(position=btn_pos)
                # Display press on GUI
                window.display_press(btn_pos)
        except serial.serialutil.SerialException as e:
            print("Device disconnected?")
            print(e)
            handle_close(macro_manager)
            return
    # end loop
# arduino_listen_loop


def get_btn_pos(data: str, macro_manager: MacroManager) -> int:
    """Parse button position from serial data that's a number
    (checks for macro_manager.config.actions.keys())
    Params:
        data - str, serial's readline that's been stripped
    Returns:
        int - btn_pos, 1 indexed
    """
    # NOTE: button position is NOT 0 indexed!
    btn_pos = int(data)
    if btn_pos > len(macro_manager.config.actions.keys()):
        # 11 => 1
        if len(str(btn_pos)) > 1:
            btn_pos = int(str(btn_pos)[-1])
    return btn_pos
# get_btn_pos


def handle_close(macro_manager: MacroManager):
    """
    Handles the close button operation, cleanup stuff
    TODO: Fix this!
    """
    if thread1 is not None:
        do_close = True
        macro_manager.root_win.destroy()
        sys.exit(0)
    else:
        print("thread is none")
        macro_manager.root_win.destroy()
        sys.exit(0)
    # stop thread1
# end handle_close

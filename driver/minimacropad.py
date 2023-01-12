#!/usr/bin/env python3
# minimacropad.py - A python driver to provide functionality to the mini macro pad.

import time
import signal
import sys
import os

import serial
import serial.tools.list_ports
from playsound import playsound

from util import MACRO_ITEMS, CustomSerialException, SerialNotFoundException, SerialMountException
from tkinter import Tk, ttk, messagebox

DEBUG = True
SECOND_MONITOR = False
RETRY_COUNT = 5
ICON_PATH = 'bell.ico'
SFX_PATH = 'snap.mp3'
SERIAL_QRY = "Arduino Leonardo"
SERIAL_BAUD = 9600
SERIAL_TIMEOUT = 0.1
MSGBOX_TITLE = "MiniMacroPad - Serial Exception"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)) + "\\res")
    return os.path.join(base_path, relative_path)


def main():
    """
    Main function
    TODO: Make this OOP instead of using global vars and constants
    """
    if DEBUG:
        print("Driver for macro pad:")
    for tries in range(RETRY_COUNT):
        try:
            arduino = init_arduino()
            # macro_display = init_gui()  # sets global root, returns MacroDisplay
        except serial.SerialException as e:
            print(e)
            messagebox.showerror(title=MSGBOX_TITLE,
                                 message=f"{str(e)}\n\nCheck if you have another instance open?")
            exit(0)
        except CustomSerialException as e:
            print(e)
            do_try_again = messagebox.askyesno(title=MSGBOX_TITLE,
                                               message=f"{str(e)}\n\nWant to try loading again?")
            if do_try_again:
                continue
            else:
                exit(0)
            exit(0)
        except Exception as e:
            print(e)
            raise e
            sys.exit(1)
        # break if trying succeeds
        break

    main_loop(arduino)
# end main


def init_arduino() -> serial.Serial:
    """
    Initialize serial COM port and return it. Uses SERIAL_QRY to find the port 
    Returns:
        Serial object of arduino / teensy
    """
    # what my PC says the teensy LC is called, could use COM7 but that could change
    signal.signal(signal.SIGINT, signal.default_int_handler)
    serial_port = load_port(SERIAL_QRY, False, DEBUG)

    if serial_port is None:
        raise SerialNotFoundException(
            f"Failed to load serial port: {SERIAL_QRY}")

    arduino = serial.Serial(port=serial_port, baudrate=SERIAL_BAUD,  timeout=SERIAL_TIMEOUT)
    if arduino is None:
        raise SerialMountException(
            f"Failed to mount Serial port: {SERIAL_QRY}")

    return arduino
# end init_arduino


# def init_gui() -> MacroDisplay:
#     """
#     Initialize the gui, uses global root var. 
#     Returns:
#         MacroDisplay object for GUI
#     """
#     global root
#     root = Tk()
#     s = ttk.Style()
#     s.configure('.', font=('Ubuntu-Mono', 16), relief='flat',
#                 foreground='#cccccc', background='#252525')
#     s.configure('TFrame', foreground='#ffffff', background='#222222')

#     main_frame = ttk.Frame(root)
#     main_frame.pack()

#     macro_display = MacroDisplay(main_frame, "MODE")

#     root.protocol("WM_DELETE_WINDOW", handle_close)
#     root.iconbitmap(resource_path(ICON_PATH))
#     root.resizable(False, False)
#     root.title("Keeb")

#     posX = None
#     posY = None

#     # Set window location + size
#     if SECOND_MONITOR:
#         posX = root.winfo_screenwidth() + int(root.winfo_screenwidth() / 2)
#         posY = root.winfo_screenheight() - int(root.winfo_screenheight() / 2)
#     else:
#         posX = int(root.winfo_screenwidth() / 2)
#         posY = int(root.winfo_screenheight() / 2)
#     root.geometry(f"475x280+{posX}+{posY}")
#     return macro_display
# # end init_gui


def main_loop(arduino):
    """
    Handles serial comms
    """
    while True:
        data = str(arduino.readline().decode().strip())
        if data != "" and DEBUG:
            print(data)
        # Do something here
    # end loop
# end main_loop


def load_port(name: str, is_COM_name: bool = True, verbose: bool = False) -> str:
    """
    Gets the COM port as a str that the teensy is connected to
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

if __name__ == "__main__":
    main()

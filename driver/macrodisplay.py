#!/usr/bin/env python3
# macrodisplay.py  - display what the macros actually are on a component
from tkinter import StringVar, Tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from util import Util
import time
from functools import partial


class MacroDisplay(ttk.Frame):
    """
    TK Frame class for the Macro Display
    Params:
        container - Tk root container
        mode - str mode to cross reference against MACRO_ITEMS
        **options - other options to be passed to tk
    Methods:
        update_mode - update the mode and rebuild grid with new data. Cross references MACRO_ITEMS
    """

    def __init__(self, container: Tk, grid_size: dict, macro_items: list, util: Util, verbose: bool = False, **options):
        """
        Constructor. Expects TK container, and grid_size like {"x": 2, "y": 3}
        """
        super().__init__(container, **options)
        ttk.Style().configure("TButton", font="Ubuntu-Mono 14")
        self.verbose = verbose
        self.util = util
        self.macro_items = macro_items
        self.truncate_length = 28
        self.container = container
        self.size = grid_size
        self.grid(column=grid_size['x'], row=grid_size['y'])
        self.macrogrid = self._init_grid()
    # end __init__

    def _init_grid(self, verbose: bool = False) -> dict:
        """
        Initializes the grid.
        Params:
            verbose - bool [False] add verbosity
        Returns:
            dict of ttk grid buttons
        """
        grid = {}
        r = 0
        c = 0
        for item in self.macro_items:
            if self.verbose:
                print(f"{item['text'].strip()} - r: {r}, c: {c}")
                print(item)

            grid[item['pos']] = ttk.Button(self.container,
                                            text=item['text'].strip(), 
                                            bootstyle=(DARK),
                                            command=partial(self.handle_press, item["pos"])
                                            )

            grid[item["pos"]].grid(row=r, column=c,
                                   ipadx=5, ipady=5, padx=2, pady=2
                                   )
            # Increment
            if item["pos"] % self.size['x'] == 0:
                r += 1
                c = 0
            else:
                c += 1
        return grid
    # end _init_grid

    def handle_press(self, position: int):
        if self.verbose:
            print(f"clicked {position}")
        self.util.handle_btn_press(position - 1)
    # handle_press

    def click(self, pos: int, verbose: bool = False):
        if self.verbose:
            print(f"click - pos: {pos}") 
        if pos > len(self.macrogrid):
            print("Hit a button that's not defined in the config file!")
            print(f"  pos: {pos} larger than buttons length")
            print("  Doing nothing!")
            return
        self.macrogrid[pos].configure(bootstyle=PRIMARY)
        time.sleep(.25)
        self.macrogrid[pos].configure(bootstyle=DARK)
    # click
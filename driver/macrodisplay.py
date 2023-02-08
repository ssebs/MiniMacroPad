#!/usr/bin/env python3
# macrodisplay.py  - display what the macros actually are on a component
import time

import ttkbootstrap as ttk
from tkinter import StringVar, Tk
from ttkbootstrap.constants import *
from functools import partial

from util import Util


class MacroDisplay(ttk.Frame):
    """
    TK Frame class for the Macro Display
    Params:
        container - Tk, root container
        grid_size - dict, size of the grid in {"x": 3,"y": 4} format
        buttons - list, list of macro items / button objects
        util - Util, util object
        verbose - bool, verbosity
        **options - other options to be passed to tk
    Methods:
        tbd
    """

    def __init__(self, container: Tk, grid_size: dict, buttons: list, util: Util, verbose: bool = False, **options):
        super().__init__(container, **options)
        ttk.Style().configure("TButton", font="Ubuntu-Mono 14")
        self.verbose = verbose
        self.util = util
        self.buttons = buttons
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
        if self.verbose:
            print("init grid:")
        grid = {}
        r = 0  # current row
        c = 0  # current column
        for idx, item in enumerate(self.buttons, start=1):
            if self.verbose:
                print(f"idx: {idx} {item['text'].strip()} - r: {r}, c: {c}")
                print("  ", end='')
                print(item)

            grid[idx] = ttk.Button(self.container,
                                   text=item['text'].strip(),
                                   bootstyle=(DARK),
                                   command=partial(
                                       self.handle_press, idx)
                                   )

            grid[idx].grid(row=r, column=c,
                           ipadx=5, ipady=5, padx=2, pady=2
                           )
            # Increment
            if idx % self.size['x'] == 0:
                r += 1
                c = 0
            else:
                c += 1
        return grid
    # end _init_grid

    def handle_press(self, position: int):
        # TODO: rename
        """Handle button click on GUI"""
        if self.verbose:
            print(f"clicked {position}")
        # alt + tab back to whatever the user was doing before
        self.util.alt_tab()
        # do function
        self.util.handle_btn_press(position)
    # handle_press

    def display_click(self, position: int, verbose: bool = False):
        # TODO: rename
        """Display visual click on GUI in `position`"""
        if self.verbose:
            print(f"click - pos: {position}")
        if position > len(self.macrogrid):
            print("Hit a button that's not defined in the config file!")
            print(f"  position: {position} larger than buttons length")
            print("  Doing nothing!")
            return
        self.macrogrid[position].configure(bootstyle=PRIMARY)
        time.sleep(.25)
        self.macrogrid[position].configure(bootstyle=DARK)
    # click

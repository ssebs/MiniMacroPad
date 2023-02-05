#!/usr/bin/env python3
# macrodisplay.py  - display what the macros actually are on a component
from tkinter import StringVar, Tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import time


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

    def __init__(self, container: Tk, grid_size: dict, macro_items: list, **options):
        """
        Constructor. Expects TK container, and grid_size like {"x": 2, "y": 3}
        """
        super().__init__(container, **options)
        ttk.Style().configure("TButton", font="Ubuntu-Mono 14")
        self.macro_items = macro_items
        self.truncate_length = 28
        self.container = container
        self.title = StringVar(value="<>")
        self.status = StringVar(value="<>")

        # TODO: Support more than 1 grid size
        self.size = grid_size
        self.grid(column=grid_size['x'], row=grid_size['y'])
        # self.grid(column=2, row=3)
        # self.size = {"x": 2, "y": 3}

        self.macrogrid = self._init_grid(verbose=True)
        self.lbl = ttk.Button(
            self.container, textvariable=self.title, bootstyle=(SECONDARY, OUTLINE), command=lambda : self.click(3))
        self.lbl.grid(row=0, column=0, padx=0, pady=0)

        self.status_lbl = ttk.Button(
            self.container, textvariable=self.status, bootstyle=(SECONDARY, OUTLINE))
        self.status_lbl.grid(row=0, column=1, padx=0, pady=0)
    # end __init__

    def _init_grid(self, verbose: bool = False) -> dict:
        # TODO add option for val strings
        """
        Initializes the grid using self.mode's value cross referenced with self.macro_items' items
        Params:
            verbose - bool [False] add verbosity
        Returns:
            dict of ttk grid buttons
        """
        # TODO: use self.grid instead...
        grid = {}
        # r = self.size["y"]
        r = 1
        c = 0
        for item in self.macro_items:
            if verbose:
                print(f"{item['text'].strip()} - r: {r}, c: {c}")
                print(item)

            grid[item['pos']] = ttk.Button(
                self.container, text=item['text'].strip(), bootstyle=(DARK))

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

    def click(self, pos: int, verbose: bool = False):
        if verbose:
            print(f"pos: {pos}") 
        self.macrogrid[pos].configure(bootstyle=PRIMARY)
        time.sleep(.25)
        self.macrogrid[pos].configure(bootstyle=DARK)
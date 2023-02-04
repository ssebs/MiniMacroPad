#!/usr/bin/env python3
# macrodisplay.py  - display what the macros actually are on a component
from tkinter import StringVar, Tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import time
from util import MACRO_ITEMS, MyLabel


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

    def __init__(self, container: Tk, **options):
        """
        Constructor
        """
        super().__init__(container, **options)
        ttk.Style().configure("TButton", font="Ubuntu-Mono 14")
        self.truncate_length = 28
        self.container = container
        self.title = StringVar(value="Title")
        self.status = StringVar(value="Status")

        self.grid(column=2, row=3)
        self.size = {"x": 2, "y": 3}

        self.macrogrid = self._init_grid(verbose=True)
        self.lbl = ttk.Button(
            self.container, textvariable=self.title, bootstyle=(LIGHT, OUTLINE), command=lambda : self.click(3))
        self.lbl.grid(row=0, column=0, padx=0, pady=0)

        self.status_lbl = ttk.Button(
            self.container, textvariable=self.status, bootstyle=(LIGHT, OUTLINE))
        self.status_lbl.grid(row=0, column=1, padx=0, pady=0)
    # end __init__

    def _init_grid(self, verbose: bool = False) -> dict:
        # TODO add option for val strings
        """
        Initializes the grid using self.mode's value cross referenced with MACRO_ITEMS' items
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
        for item in MACRO_ITEMS:
            if verbose:
                print(f"{item['text']} - r: {r}, c: {c}")

            grid[item['pos']] = ttk.Button(
                self.container, text=item['text'].strip(), bootstyle=(DARK))

            grid[item["pos"]].grid(row=r, column=c,
                                   ipadx=5, ipady=5, padx=0, pady=0
                                   )
            # Increment
            if item["pos"] % 2 == 0:
                r += 1
                c = 0
            else:
                c += 1
        return grid
    # end _init_grid

    def click(self, pos):
        print(f"pos: {pos}") 
        self.macrogrid[pos].configure(bootstyle=PRIMARY)
        time.sleep(.25)
        self.macrogrid[pos].configure(bootstyle=DARK)
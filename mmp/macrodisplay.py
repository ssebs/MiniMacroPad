#!/usr/bin/env python3
# macrodisplay.py  - TK Frame main window for the Macro Display
import time

import ttkbootstrap as ttk
from tkinter import Tk
from ttkbootstrap.constants import *
from functools import partial

from mmp.macromanager import MacroManager


class MacroDisplay(ttk.Frame):
    """
    TK Frame main window for the Macro Display
    Params:
        container - Tk, root container
        macro_manager - MacroManager, reference to the MacroManager
        verbose - bool [False], verbosity
        **options - other options to be passed to tk
    Methods:
        tbd
    """

    def __init__(self, macro_manager: MacroManager, verbose: bool = False, **options):
        super().__init__(macro_manager.root_win, **options)
        ttk.Style().configure("TButton", font="Ubuntu-Mono 14")
        self.macro_manager: MacroManager = macro_manager
        self.container: Tk = macro_manager.root_win
        self.verbose: bool = macro_manager.verbose

        self.size: dict = macro_manager.config.size
        self.actions: list = macro_manager.config.actions

        self.truncate_length = 28  # TODO: make a param
        self.grid(column=self.size['x'], row=self.size['y'])
        self.macrogrid = self._init_grid()
    # __init__

    def _init_grid(self, verbose: bool = False) -> dict:
        """
        Initializes the grid.
        Params:
            verbose - bool [False], verbosity
        Returns:
            dict of ttk grid buttons
        """
        if self.verbose:
            print("init grid:")
        grid = {}
        r = 0  # current row
        c = 0  # current column
        for idx, item in enumerate(self.actions.keys(), start=1):
            if self.verbose:
                print(f"idx: {idx} {item.strip()} - r: {r}, c: {c}")
                print("  ", end='')
                print(item)

            # is_recording_macro: bool = ("rec" in item["func"])
            do_alt_tab = True  # TODO: replace with is gui flag?

            grid[idx] = ttk.Button(self.container,
                                   text=item.strip(),
                                   bootstyle=(DARK),
                                   command=partial(
                                       self._handle_gui_press, position=idx, do_alt_tab=do_alt_tab)
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
    # _init_grid

    def _handle_gui_press(self, position: int, do_alt_tab: bool = False):
        """Handle button click on GUI
        TODO: fix desc
        Params:
            position - int, position within buttons[] that was pressed
            do_alt_tab - bool [False], run alt + tab before the macro
        """
        if self.verbose:
            print(f"Clicked {position}")
        if do_alt_tab:
            # alt + tab back to whatever the user was doing before
            self.macro_manager.run_action(
                action_name="KB_SEND_HOTKEY",
                value=["alt", "tab"]
            )

        # Run the actual action
        self.macro_manager.run_action(position=position)
    # _handle_gui_press

    def display_press(self, position: int, verbose: bool = False):
        """Display visual click on GUI in position var
        Params:
            position - int, position within buttons[] that was pressed
            verbose - bool [False], verbosity
        """
        if self.verbose:
            print(f"click - pos: {position}")
        if position > len(self.macrogrid):
            print("Hit a button that's not defined in the config file!")
            print(f"  position: {position} larger than buttons length")
            print("  Doing nothing!")
            return
        self.macrogrid[position].configure(bootstyle=PRIMARY)
        time.sleep(.25)  # TODO: make this a variable
        self.macrogrid[position].configure(bootstyle=DARK)
    # display_press

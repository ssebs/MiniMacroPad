#!/usr/bin/env python3
# guimanager.py - Manager for the GUI elements of the MiniMacroPad
import signal

from typing import Optional

from mmp.macrodisplay import MacroDisplay
from mmp.macromanager import MacroManager
from mmp.util import (
    resource_path, ICON_PATH
)


class GUIManager():
    """Initialize & manage the GUI"""

    def __init__(self, macro_manager: MacroManager, cli_arg_monitor_num: Optional[int]):
        """Create GUIManager
        (Instantiates a MacroDisplay object)
        Params:
            macro_manager - MacroManager, instance of the MacroManager class that's used elsewhere in the program
            cli_arg_monitor_num - Optional[int], Which monitor to show the GUI on. If None, use what's in the config file
        """
        self.macro_manager: MacroManager = macro_manager

        self.monitor_num: int = self._get_monitor_number(cli_arg_monitor_num)
        self.macro_display: MacroDisplay = self._setup_window()
    # __init__

    def _get_monitor_number(self, cli_arg_monitor_num: Optional[int]) -> int:
        """Get Monitor Number"""
        # Save monitor_num in the config file if they've defined it.
        if cli_arg_monitor_num:
            self.macro_manager.config.config["MONITOR"] = int(monitor_num)
            self.macro_manager.config.save_config()
        return self.macro_manager.config.config["MONITOR"]
    # _get_monitor_number

    def _setup_window(self) -> MacroDisplay:
        """
        docstring
        """
        # Create main window
        macro_display = MacroDisplay(macro_manager=self.macro_manager)

        # Set flags for handling closing the window
        signal.signal(signal.SIGINT, signal.default_int_handler)
        # TODO: Fix the threading to uncomment this!
        # self.macro_manager.root_win.protocol("WM_DELETE_WINDOW", partial(handle_close, self.macro_manager))

        # Set icon / title
        self.macro_manager.root_win.iconbitmap(resource_path(ICON_PATH))
        # macro_manager.root_win.resizable(False, False)
        self.macro_manager.root_win.title("MiniMacroPad")

        # TODO: Make this easier to read!
        posX = None
        posY = None
        # Set window location + size
        # TODO: Support more than 2 monitors
        if self.macro_manager.config.config["MONITOR"] == -1:
            # dev mode
            posX = self.macro_manager.root_win.winfo_screenwidth() + 200
            posY = int(self.macro_manager.root_win.winfo_screenheight() / 2) - 200
        elif self.macro_manager.config.config["MONITOR"] != 1:
            # 2nd monitor
            posX = self.macro_manager.root_win.winfo_screenwidth(
            ) + int(self.macro_manager.root_win.winfo_screenwidth() / 2)
            posY = self.macro_manager.root_win.winfo_screenheight(
            ) - int(self.macro_manager.root_win.winfo_screenheight() / 2)
        else:
            # 1st monitor
            posX = int(self.macro_manager.root_win.winfo_screenwidth() / 2)
            posY = int(self.macro_manager.root_win.winfo_screenheight() / 2)

        # Set position & size
        self.macro_manager.root_win.geometry(
            f"{self.macro_manager.config.config['GUI_SIZE']}+{posX}+{posY}")

        return macro_display
    # _setup_window

    def show_dialog(self, title: str):
        """
        TODO: implement
        """
        pass
# GUIManager

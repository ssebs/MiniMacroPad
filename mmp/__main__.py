#!/usr/bin/env python3
# __main__.py - minimacropad driver python pkg
from argparse import ArgumentParser
import mmp.minimacropad

# https://stackoverflow.com/a/23891673
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


def main():
    """Parse args & run mmp main"""
    gui_only_help = "Don't try to connect to a Serial hardware device, but still open the GUI MacroPad."
    monitor_help = "Which monitor to show the gui on."
    verbose_help = "Add verbose output. Useful for debugging."

    parser = ArgumentParser(description="MiniMacroPad - GUI")
    parser.add_argument(
        "-g", "--gui-only", "--no-arduino",
        action="store_true", help=gui_only_help, default=False
    )
    parser.add_argument(
        "-m", "--monitor",
        action="store", help=monitor_help, default=None
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true", help=verbose_help, default=False
    )

    args = parser.parse_args()
    mmp.minimacropad.main(is_gui_only=args.gui_only, monitor_num=args.monitor, is_verbose=args.verbose)
# run


if __name__ == "__main__":
    main()
# __main__

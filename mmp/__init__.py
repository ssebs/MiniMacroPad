#!/usr/bin/env python3
# __init__.py - minimacropad driver python pkg
from argparse import ArgumentParser
import mmp

# https://stackoverflow.com/a/23891673
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))


def run():
    """Parse args & run main"""
    gui_only_help = "Don't try to connect to a Serial hardware device, but still open the GUI MacroPad."
    verbose_help = "Add verbose output. Useful for debugging."

    parser = ArgumentParser(description="MiniMacroPad - GUI")
    parser.add_argument("--gui-only", "--no-arduino",
                        action="store_true", help=gui_only_help, default=False)
    parser.add_argument("-v", "--verbose",
                        action="store_true", help=verbose_help, default=False)

    args = parser.parse_args()
    mmp.main(is_gui_only=args.gui_only, is_verbose=args.verbose)


if __name__ == "__main__":
    run()
# __main__

#!/usr/bin/env python3
# macromanager.py - Manager for the Macros for use with the MiniMacroPad
import keyboard
import mouse
import time

from datetime import datetime
from enum import Enum
from tkinter import Tk
from typing import Tuple, Dict, List, Union, Any

from mmp.config import Config
from mmp.stringlooper import StringLooper
from mmp.actionmanager import ActionManager


class FuncManager():
    """
    NOTE: This is being replaced by ActionManager! This is only for reference while implementing the looper stuff
    """

    def __init__(self, config: Config, default_delay: float = 0.2, verbose: bool = False):
        self.verbose: bool = verbose
        self.config: Config = config
        self.default_delay: float = default_delay
        self.loopers: Dict[StringLooper] = self._parse_loopers()
    # __init__

    def _parse_loopers(self) -> dict:
        """parse config json to create string loopers
        (Instantiates StringLooper objects)
        Returns:
            dict[str, StringLooper]
        """
        # TODO: fix the exception handling! make it return an error instead of raising here
        _looper = {}
        # TODO: reimplement
        for btn in self.config.buttons:
            if "extra" not in btn:
                continue
            try:
                # If the array name is not in data
                if btn["extra"] not in self.config.data:
                    raise Exception(
                        f"Failed to find {btn['extra']} in {self.config.data}")
                # Get array name from extra variable
                tmp_loop = StringLooper(self.config.data[btn['extra']])
                # Add to dict
                _looper[btn['extra']] = tmp_loop

            except Exception as e:
                print("Failed to add looper")
                raise e

        if self.verbose:
            print("loopers:")
            for looper in _looper.values():
                print(looper)

        # Return new dict
        return _looper
    # _parse_loopers

    def loop_up(self, idx: int, extra: str):
        self.loopers[extra].loop_up()
        if self.verbose:
            print(
                f"loop_up: {self.loopers[extra].get_str()}, idx: {idx}, extra: {extra}")
        keyboard.write(self.loopers[extra].get_str())
    # loop_up func from json

    def loop_down(self, idx: int, extra: str):
        self.loopers[extra].loop_down()
        keyboard.write(self.loopers[extra].get_str())
    # loop_down func from json

    def loop_rand(self, idx: int, extra: str):
        self.loopers[extra].loop_rand()
        keyboard.write(self.loopers[extra].get_str())
    # loop_rand func from json

# FuncManager


class MacroManager():
    """Manager for the Macros for use with the MiniMacroPad"""

    def __init__(self, root_win: Tk, config_path: str = None, verbose: bool = False):
        """Create MacroManager
        (Instantiates Config, ActionManager objects)
            Params:
                root_win - Tk, root container
                config_path - str [None], path to config, if None use default
                verbose - bool [False], verbosity
            Methods that you should use:
                run_action
        """
        self.verbose: bool = verbose

        # Load json Config from file, takes config_path if provided
        self.config: Config = Config(config_path=config_path, verbose=verbose)

        # Setup the class that will run the macro itself
        self.action_manager: ActionManager = ActionManager(self.config, verbose=verbose)

        # Set root_win from param
        self.root_win: Tk = root_win

        # The last pressed button position on the macro pad
        self.last_pressed_pos = -1
    # __init__

    def run_action(self, position: int = -1, action_name: str = None, value: Any = None):
        """Run an action depending on the action type
        TODO: support delays here (e.g. alt tab)
        Params:
            position - int [-1], position where to call the action function from
        """
        if self.verbose:
            print(f"Running button press for {position}")

        # Run action_name if defined, don't use the button position at all!
        if action_name:
            if value is None:
                raise Exception(f"Value cannot be None for {action_name}!")
            self.action_manager.actions[action_name](value)
            return

        # Otherwise, run the action from the last pressed position
        self.last_pressed_pos = position
        action_name, action_items = self._get_action_from_pos()
        if action_name == "err":
            print(action_items)
            return
        elif action_items is None:
            print(f"Could not get action at pos: {position}. Make sure it's in ACTIONS in the config. Or is it 0? It should start at 1")
            return

        # For every _action in action_items, run the func
        for _action in action_items:
            func_name, func_value = next(iter(_action.items()))
            self.action_manager.actions[func_name](func_value)

        # # TODO: support mouse recording
        # # TODO: try/catch
        # # TODO: add recording action for KB!
    # run_action

    def rec_mouse(self, idx: int):
        """Record mouse inputs
        TODO: Reimplement
        """
        positions: Dict[str, str] = {}
        has_quit: bool = False
        count: int = 0

        def add_pos(_type: str):
            # Add mouse position and button click to positions
            # _type can be: left, right, double, middle
            x, y = mouse.get_position()
            now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%Z")
            positions[str(now)] = {
                "type": _type,
                "posx": x,
                "posy": y,
            }

        while not has_quit and count < 999999999:
            # Record user input until they hit "ESC"
            count += 1
            if self.verbose:
                print(f"rec_mouse # {count}")
            has_quit = keyboard.is_pressed("escape")

            mouse.on_click(partial(add_pos, "left"))
            mouse.on_middle_click(partial(add_pos, "middle"))
            mouse.on_right_click(partial(add_pos, "right"))
            mouse.on_double_click(partial(add_pos, "double"))
            time.sleep(0.02)

        keyboard.unhook_all()
        mouse.unhook_all()
        if self.verbose:
            print("Positions")
            print(positions)
        self.config.full_config["BUTTONS"][idx]["mouse_movements"] = positions
        self.config.save_config()
    # rec_mouse

    def _get_action_from_pos(self) -> Tuple[str, Union[Dict[str, Any], str]]:
        """Get action name & action object from self.last_pressed_pos
        Returns:
            Tuple[str, Union[Dict[str, Any], str]] - If the first part of the tuple is "err", then you hit an error
        """
        # Error if the user hit a button that was bigger than actions, so we can't call anything
        if self.last_pressed_pos > len(self.config.actions.keys()) or self.last_pressed_pos == 0:
            _msg = (
                "Hit a button that's not defined in the config file!"
                f"pos: {self.last_pressed_pos} larger than buttons length"
                "Doing nothing"
            )
            return ("err", _msg)

        _action_matched_key = None
        _action = None

        for idx, action_key in enumerate(self.config.actions.keys(), start=1):
            if idx == self.last_pressed_pos:
                _action_matched_key = action_key
                _action = self.config.actions[action_key]
                break
        return (_action_matched_key, _action)
    # _get_action_from_pos

# MacroManager

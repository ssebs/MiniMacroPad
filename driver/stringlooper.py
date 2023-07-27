#!/usr/bin/env python3
# stringlooper.py - StringLooper class
import random
from typing import List


class StringLooper():
    """Manages the state of looping thru a list"""

    def __init__(self, strings: List[str]):
        """Manages the state of looping thru a list
        Params:
            strings - list[str], List of strings to loop thru
        """
        self.strings: List[str] = strings
        self.max: int = len(strings) - 1
        self.min: int = 0
        self.pos: int = 0
    # __init__

    def get_str(self) -> str:
        """Get the string at self.pos (current position)
        Returns:
            str, string at current position
        """
        return self.strings[self.pos]
    # get_str

    def loop_up(self) -> None:
        """Loop up thru self.strings"""
        if self.pos >= self.max:
            self.pos = 0
            return
        self.pos += 1
    # loop_up

    def loop_down(self) -> None:
        """Loop down thru self.strings"""
        if self.pos <= 0:
            self.pos = self.max
            return
        self.pos -= 1
    # loop_down

    def loop_rand(self):
        """Randomly change self.pos for looping thru self.strings"""
        self.pos = random.randint(self.min, self.max)
    # loop_rand

    def __repr__(self) -> None:
        """Print all relevant data for this looper to stdout"""
        print(self.__str__)
    # __repr__

    def __str__(self) -> str:
        """Get all relevant data for this looper
        Returns:
            str, list of strings, positional info as 1 string.
        """
        return f"{str(self.strings)}, pos: {self.pos}, min: {self.min}, max: {self.max}"
    # __str__

# StringLooper

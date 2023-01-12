#!/usr/bin/env python3
# util.py - Util stuff
from enum import Enum
from tkinter import ttk

MACRO_ITEMS = [
    {
        "pos": 1,
        "text": "Test"
    },
    {
        "pos": 2,
        "text": "Foo"
    },
    {
        "pos": 3,
        "text": "Bar"
    },
    {
        "pos": 4,
        "text": "undo"
    }
]


class CustomSerialException(Exception):
    pass


class SerialNotFoundException(CustomSerialException):
    pass


class SerialMountException(CustomSerialException):
    pass


class MyLabel(ttk.Frame):
    '''inherit from Frame to make a label with customized border'''

    def __init__(self, parent, myborderwidth=0, color=None,
                 myborderplace='center', *args, **kwargs):
        s = ttk.Style()
        s.configure('TFrame', background=color)
        self.frame = ttk.Frame.__init__(self, parent)
        self.propagate(False)  # prevent frame from auto-fitting to contents
        self.label = ttk.Label(self.frame, *args, **kwargs)  # make the label

        # pack label inside frame according to which side the border
        # should be on. If it's not 'left' or 'right', center the label
        # and multiply the border width by 2 to compensate
        if myborderplace == 'left':
            self.label.pack(side=RIGHT)
        elif myborderplace == 'right':
            self.label.pack(side=LEFT)
        else:
            self.label.pack()
            myborderwidth = myborderwidth * 2

        # set width and height of frame according to the req width
        # and height of the label
        self.config(width=self.label.winfo_reqwidth() + myborderwidth)
        self.config(height=self.label.winfo_reqheight())

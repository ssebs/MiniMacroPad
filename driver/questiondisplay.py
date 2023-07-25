#!/usr/bin/env python3
# questiondisplay.py  - display a notice
import time
from typing import List, Callable
import ttkbootstrap as ttk
from tkinter import StringVar, Tk, Toplevel
from ttkbootstrap.constants import *
from functools import partial


class QuestionDisplay(ttk.Frame):
    """
    TK Frame class for the Question Display
    Params:
        container - Tk, root container
        question - str, Question to ask the user
        answers - List[str], List of possible answers
        callback - Callable[str], Callback function, returns the selected answer as a str
        verbose - bool, verbosity
        **options - other options to be passed to tk
    Methods:
        tbd
    """

    def __init__(self, question: str, answers: List[str], callback: Callable, verbose: bool = False, **options):
        container = ttk.Window(themename="darkly")
        super().__init__(container, **options)
        ttk.Style().configure("TButton", font="Ubuntu-Mono 14")
        ttk.Style().configure("TLabel", font="Ubuntu-Mono 12")
        self.container = container
        self.question = question
        self.answers = answers
        self.callback = callback
        self.verbose = verbose
        self._init_gui()
        self.container.attributes('-topmost', True)
        self.container.update()
        self.container.mainloop()
    # end __init__

    def _handle_press(self, answer: str):
        self.callback(answer)
        self.container.quit()
        self.container.destroy()

    def _init_gui(self, verbose: bool = False) -> None:
        """
        Initializes the answers in the combobox.
        Params:
            verbose - bool [False] add verbosity
        Returns:
            None
        """
        if self.verbose:
            print("init gui")

        question_txt = ttk.Label(self.container, text=self.question).pack(
            padx=5, pady=10, side="top")

        for answer in self.answers:
            answer_btn = ttk.Button(self.container,
                                    text=answer,
                                    bootstyle=(DARK),
                                    command=partial(self._handle_press, answer)
                                    ).pack(padx=5, pady=5, side="left", expand=True)

    # _init_gui


if __name__ == "__main__":
    question_display = QuestionDisplay(
        question="Would you like that to be a left, right, or double click?", answers=["Left", "Right", "Double"], callback=print)

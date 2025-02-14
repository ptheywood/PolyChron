#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 17:43:25 2021

@author: bryony
"""

import os
import pathlib
import tkinter as tk
from tkinter import ttk
import copy
import re
import ast
import matplotlib as plt
from PIL import Image, ImageTk, ImageChops
from networkx.drawing.nx_pydot import read_dot, write_dot
import networkx as nx
import pydot
import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfile
from graphviz import render
from . import automated_mcmc_ordering_coupling_copy as mcmc
from ttkthemes import ThemedStyle
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pickle
from tkinter import simpledialog
import tkinter.font as tkFont
from tkinter.messagebox import askquestion
import csv
from importlib.metadata import version  # requires python >= 3.8
import argparse

from .globals import *
from .StdoutRedirector import *
from .Util import *
from .popupWindow import *
from .popupWindow2 import *
from .popupWindow3 import *
from .popupWindow4 import *
from .popupWindow5 import *
from .popupWindow6 import *
from .popupWindow7 import *
from .popupWindow8 import *
from .popupWindow9 import *
from .popupWindow10 import *
from .load_Window import *
from .MainFrame import *
from .StartPage import *
from .PageOne import *
from .PageTwo import *


# Global scoping of MAIN_FRAME is currently required for state saving behaviour, prior to refactoring.
MAIN_FRAME = MainFrame()
style = ThemedStyle(MAIN_FRAME)
style.set_theme("arc")
# f = tkFont.Font(family='helvetica', size=10, weight='bold')
# s = ttk.Style()
# s.configure('.', font=f)
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=12, weight="bold")
style = ttk.Style(MAIN_FRAME)
style.configure("TEntry", font=("Helvetica", 12, "bold"))
style.configure("TButton", font=("Helvetica", 12, "bold"))
style.configure("TLabel", font=("Helvetica", 12, "bold"))
style.configure("TOptionMenu", font=("Helvetica", 12, "bold"))
style.configure("TTreeView", font=("Helvetica", 12, "bold"))
MAIN_FRAME.option_add("*Font", default_font)
MAIN_FRAME.geometry("2000x1000")
MAIN_FRAME.title(f"PolyChron {version('PolyChron')}")


def parse_cli(argv=None):
    """Parse and return command line arguments

    Args:
        argv (list[str] or None): optional list of command line parameters to parse. If None, sys.argv is used by `argparse.ArgumentParser.parse_args`

    Returns:
        (argparse.Namespace): Namespace object with arguments set as attributes, as returned by `argparse.ArgumentParser.parse_args()`
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="store_true", help="show version information and exit")
    args = parser.parse_args(argv)
    return args


def print_version():
    """Print the version of PolyChron to stdout

    Note:
        For editable installs the printed value may be incorrect
    """
    print(f"PolyChron {version('PolyChron')}")


def main():
    """Main method as the entry point for launching the GUI"""
    args = parse_cli()
    if args.version:
        print_version()
    else:
        MAIN_FRAME.mainloop()


# If this script is executed directly, run the main method
if __name__ == "__main__":
    main()

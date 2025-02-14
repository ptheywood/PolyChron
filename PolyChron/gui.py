#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 17:43:25 2021

@author: bryony
"""

from tkinter import ttk
from ttkthemes import ThemedStyle
import tkinter.font as tkFont
from importlib.metadata import version  # requires python >= 3.8
import argparse

from .MainFrame import MainFrame


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

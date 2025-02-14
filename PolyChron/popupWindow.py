
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
from .Util import *

class popupWindow(object):
    def __init__(self, master):
        """initialises popupWindow"""
        self.top = tk.Toplevel(master)
        self.top.configure(bg="#AEC7D6")
        self.top.geometry("1000x400")
        # pop up window to allow us to enter a context that we want to change the meta data for
        self.l = ttk.Label(self.top, text="Context Number")
        self.l.pack()
        self.e = ttk.Entry(self.top)  # allows us to keep t6rack of the number we've entered
        self.e.pack()
        self.b = ttk.Button(self.top, text="Ok", command=self.cleanup)  # gets ridof the popup
        self.b.pack()
        self.value = tk.StringVar(self.top)

    def cleanup(self):
        """destroys popupWindow"""
        self.value = self.e.get()
        self.top.destroy()
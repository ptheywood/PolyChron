
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
from .load_Window import *

# mainframe is the parent class that holds all the other classes
class MainFrame(tk.Tk):
    def __init__(self, *args, **kwargs):
        """initilaises the main frame for tkinter app"""
        tk.Tk.__init__(self, *args, **kwargs)
        os.chdir(POLYCHRON_PROJECTS_DIR)
        load_Window(self)
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()
        frame.config()

    def get_page(self, page_class):
        """Shows the desired frame"""
        return self.frames[page_class]
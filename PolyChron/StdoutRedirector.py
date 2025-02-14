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

class StdoutRedirector(object):
    def __init__(self, text_area, pb1):
        """allows us to rimedirect
        output to the app canvases"""
        self.text_area = text_area
        self.pb1 = pb1

    def write(self, str):
        """writes to canvas"""
        #     self.text_area.update_idletasks()
        self.pb1.update_idletasks
        # self.text_area.destroy()
        str1 = re.findall(r"\d+", str)
        if len(str1) != 0:
            self.text_area["text"] = str1[0] + "% complete"
            self.pb1["value"] = int(str1[0])
            self.text_area.update_idletasks()
        #  self.text_area.see(1.0)

    def flush(self):
        pass

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

class popupWindow6(object):
    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        top.configure(bg="white")
        self.top.geometry("1000x400")
        self.top.title("Removal of stratigraphic relationship")
        self.l = tk.Label(
            top,
            text="Why are you deleting the stratigraphic relationship between these contexts?",
            bg="white",
            font="helvetica 12",
            fg="#2f4858",
        )
        self.l.place(relx=0.3, rely=0.1)
        self.e = tk.Text(top, font="helvetica 12", fg="#2f4858")
        self.e.place(relx=0.3, rely=0.2, relheight=0.5, relwidth=0.5)
        self.b = tk.Button(top, text="OK", command=self.cleanup, bg="#2F4858", font=("Helvetica 12 bold"), fg="#eff3f6")
        self.b.place(relx=0.3, rely=0.7)

    def cleanup(self):
        self.value = self.e.get("1.0", "end")
        self.top.destroy()

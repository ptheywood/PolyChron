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

class popupWindow7(object):
    def __init__(self, master, df):
        top = self.top = tk.Toplevel(master)
        self.canvas = tk.Canvas(top, bg="white")
        top.title("Data preview")
        self.canvas.pack()
        self.l = tk.Label(self.canvas, text="Data Preview")
        self.l.pack()
        cols = list(df.columns)

        tree = ttk.Treeview(self.canvas)
        tree.pack()
        tree["columns"] = cols
        for i in cols:
            tree.column(i, anchor="w")
            tree.heading(i, text=i, anchor="w")

        for index, row in df.iterrows():
            tree.insert("", 0, text=index, values=list(row))
        tree["show"] = "headings"
        self.b = tk.Button(
            top, text="Load data", command=self.cleanup1, bg="#2F4858", font=("Helvetica 12 bold"), fg="#eff3f6"
        )
        self.b.pack()
        self.c = tk.Button(
            top, text="Cancel", command=self.cleanup2, bg="#2F4858", font=("Helvetica 12 bold"), fg="#eff3f6"
        )
        self.c.pack()

    def cleanup1(self):
        self.value = "load"
        self.top.destroy()

    def cleanup2(self):
        self.value = "cancel"
        self.top.destroy()
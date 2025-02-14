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

# Get the absolute path to a directory in the users home dir
POLYCHRON_PROJECTS_DIR = (pathlib.Path.home() / "Documents/Pythonapp_tests/projects").resolve()
# Ensure the directory exists (this is a little aggressive)
POLYCHRON_PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
# Change into the projects dir
os.chdir(POLYCHRON_PROJECTS_DIR)
old_stdout = sys.stdout

# global variables
phase_true = 0
load_check = "not_loaded"
mcmc_check = "mcmc_notloaded"
proj_dir = ""
SCRIPT_DIR = pathlib.Path(__file__).parent  # Path to directory containing this script
CALIBRATION = pd.read_csv(SCRIPT_DIR / "linear_interpolation.txt")
# Vars not previously defined in global scope but set via globals keyword
FILE_INPUT = None 
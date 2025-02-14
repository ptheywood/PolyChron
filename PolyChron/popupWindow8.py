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

class popupWindow8(object):
    def __init__(self, master, path):
        self.master = master
        self.path = path
        model_list_prev = [d for d in os.listdir(path) if os.path.isdir(path + "/" + d)]
        model_list = []
        for i in model_list_prev:
            mod_path = str(path) + "/" + str(i) + "/python_only/save.pickle"
            with open(mod_path, "rb") as f:
                data = pickle.load(f)
                load_check = data["load_check"]
            if load_check == "loaded":
                model_list.append(i)

        self.top = tk.Toplevel(master)
        self.top.configure(bg="white")
        self.top.title("Model calibration")
        self.top.geometry("1000x400")
        self.l = tk.Label(
            self.top, text="Which model/s would you like calibrate?", bg="white", font="helvetica 12", fg="#2f4858"
        )
        self.l.place(relx=0.3, rely=0.1)
        self.e = tk.Listbox(self.top, font="helvetica 12", fg="#2f4858", selectmode="multiple")
        self.e.place(relx=0.3, rely=0.2, relheight=0.5, relwidth=0.5)
        #       self.e.bind('<<ListboxSelect>>',tk.CurSelet)
        for items in model_list:
            self.e.insert("end", items)
        self.b = tk.Button(
            self.top, text="OK", command=self.cleanup, bg="#2F4858", font=("Helvetica 12 bold"), fg="#eff3f6"
        )
        self.b.place(relx=0.3, rely=0.7)
        self.b = tk.Button(
            self.top, text="Select all", command=self.selectall, bg="#2F4858", font=("Helvetica 12 bold"), fg="#eff3f6"
        )
        self.b.place(relx=0.6, rely=0.7)

    def selectall(self):
        self.e.select_set(0, "end")

    def save_state_1(self, j):
        global mcmc_check, load_check, FILE_INPUT

        vars_list_1 = dir(self)
        var_list = [
            var
            for var in vars_list_1
            if (("__" and "grid" and "get" and "tkinter" and "children") not in var) and (var[0] != "_")
        ]
        data = {}
        check_list = ["tkinter", "method", "__main__", "PIL"]
        for i in var_list:
            v = getattr(self, i)
            if not any(x in str(type(v)) for x in check_list):
                data[i] = v
        data["all_vars"] = list(data.keys())
        data["load_check"] = load_check
        data["mcmc_check"] = mcmc_check
        data["file_input"] = FILE_INPUT
        path = self.path + "/" + str(j) + "/python_only/save.pickle"
        try:
            with open(path, "wb") as f:
                pickle.dump(data, f)
            tk.messagebox.showinfo("Success", "Your model has been saved")
        except Exception:
            tk.messagebox.showerror("Error", "File not saved")

    def load_cal_data(self, j):
        global mcmc_check, load_check, FILE_INPUT
        with open(self.path + "/" + str(j) + "/python_only/save.pickle", "rb") as f:
            data = pickle.load(f)
            vars_list = data["all_vars"]
            for i in vars_list:
                setattr(self, i, data[i])
            FILE_INPUT = data["file_input"]
            load_check = data["load_check"]
            mcmc_check = data["mcmc_check"]

    def cleanup(self):
        global mcmc_check
        values = [self.e.get(idx) for idx in self.e.curselection()]
        for i in values:
            self.load_cal_data(i)
            (
                self.CONTEXT_NO,
                self.ACCEPT,
                self.PHI_ACCEPT,
                self.PHI_REF,
                self.A,
                self.P,
                self.ALL_SAMPS_CONT,
                self.ALL_SAMPS_PHI,
                self.resultsdict,
                self.all_results_dict,
            ) = self.master.MCMC_func()
            mcmc_check = "mcmc_loaded"
            self.save_state_1(i)
        self.top.destroy()

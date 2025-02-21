import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import networkx as nx
import pydot
import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfile
from . import automated_mcmc_ordering_coupling_copy as mcmc
import sys
import pickle
from tkinter.messagebox import askquestion
import csv

from .globals import phase_true, load_check, mcmc_check, proj_dir, CALIBRATION, FILE_INPUT
from .Util import clear_all, node_del_fixed, node_coords_fromjson, imagefunc, phase_labels, imgrender, imgrender2, imgrender_phase
from .popupWindow import popupWindow
from .popupWindow2 import popupWindow2
from .popupWindow3 import popupWindow3
from .popupWindow5 import popupWindow5
from .popupWindow6 import popupWindow6
from .popupWindow7 import popupWindow7
from .popupWindow8 import popupWindow8
from .popupWindow9 import popupWindow9
from .popupWindow10 import popupWindow10
from .load_Window import load_Window
from .PageTwo import PageTwo
from .StdoutRedirector import StdoutRedirector

class StartPage(tk.Frame):
    """Main frame for tkinter app"""

    def __init__(self, parent, controller):
        global load_check, mcmc_check, FILE_INPUT, proj_dir
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background="white")
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, bg="#AEC7D6")
        self.canvas.place(relx=0, rely=0.03, relwidth=1, relheight=0.97)
        self.button1 = tk.Button(
            self,
            text="Stratigraphy and supplementary data",
            font="helvetica 12 bold",
            fg="#2F4858",
            command=lambda: controller.show_frame("StartPage"),
            bd=0,
            highlightthickness=0,
            bg="#AEC7D6",
        )
        self.button1.place(relx=0.38, rely=0.0, relwidth=0.17, relheight=0.03)
        self.button1_a = tk.Button(
            self,
            text="Dating Results",
            font="helvetica 12 bold",
            fg="#8F4300",
            command=lambda: controller.show_frame("PageOne"),
            bd=0,
            highlightthickness=0,
            bg="#FFE9D6",
        )
        self.button1_a.place(relx=0.55, rely=0.0, relwidth=0.15, relheight=0.03)
        # define all variables that are used
        self.h_1 = 0
        self.w_1 = 0

        self.transx = 0
        self.transy = 0
        self.meta1 = ""
        self.mode = ""
        self.node_del_tracker = []
        ##### intial values for all the functions
        self.delnodes = []
        self.edge_nodes = []
        self.comb_nodes = []
        self.edges_del = []
        self.temp = []
        self.x_1 = 1
        self.image = "noimage"
        self.phase_rels = None
        self.chrono_dag = None
        self.imscale = 0
        self.graph = None
        self.littlecanvas_img = None
        self.width = 0
        self.height = 0
        self.delta = 0
        self.container = None
        self.datefile = None
        self.phasefile = None
        self.CONTEXT_NO = 0
        self.PHI_REF = None
        self.prev_phase = []
        self.post_phase = []
        self.ACCEPT = None
        self.PHI_ACCEPT = None
        self.resultsdict = None
        self.ALL_SAMPS_CONT = None
        self.ALL_SAMPS_PHI = None
        self.A = 0
        self.P = 0
        self.variable = 0
        self.image2 = "noimage"
        self.resultsdict = {}
        self.all_results_dict = {}
        self.treeview_df = pd.DataFrame()
        self.file_menubar = ttk.Menubutton(self, text="File")
        self.strat_check = False
        self.phase_check = False
        self.phase_rel_check = False
        self.date_check = False
        # Adding File Menu and commands
        file = tk.Menu(self.file_menubar, tearoff=0, bg="white", font=("helvetica 12 bold"))
        self.file_menubar["menu"] = file
        file.add_separator()
        FILE_INPUT = None
        file.add_command(
            label="Load stratigraphic diagram file (.dot)", command=lambda: self.open_file1(), font="helvetica 12 bold"
        )
        file.add_command(
            label="Load stratigraphic relationship file (.csv)",
            command=lambda: self.open_file2(),
            font="helvetica 12 bold",
        )
        file.add_command(
            label="Load scientific dating file (.csv)", command=lambda: self.open_file3(), font="helvetica 12 bold"
        )
        file.add_command(
            label="Load context grouping file (.csv)", command=lambda: self.open_file4(), font="helvetica 12 bold"
        )
        file.add_command(
            label="Load group relationship file (.csv)", command=lambda: self.open_file5(), font="helvetica 12 bold"
        )
        file.add_command(
            label="Load context equalities file (.csv)", command=lambda: self.open_file6(), font="helvetica 12 bold"
        )
        file.add_command(label="Load new project", command=lambda: load_Window(MAIN_FRAME), font="helvetica 12 bold")
        file.add_command(
            label="Load existing model",
            command=lambda: load_Window.load_model(load_Window(MAIN_FRAME), proj_dir),
            font="helvetica 12 bold",
        )
        file.add_command(
            label="Save changes as current model", command=lambda: self.save_state_1(), font="helvetica 12 bold"
        )
        file.add_command(
            label="Save changes as new model",
            command=lambda: self.refresh_4_new_model(controller, proj_dir, load=False),
            font="helvetica 12 bold",
        )
        file.add_separator()
        file.add_command(label="Exit", command=lambda: self.destroy1)
        self.file_menubar.place(relx=0.00, rely=0, relwidth=0.1, relheight=0.03)
        self.view_menubar = ttk.Menubutton(self, text="View")
        # Adding File Menu and commands
        file1 = tk.Menu(self.view_menubar, tearoff=0, bg="white", font=("helvetica", 11))
        self.view_menubar["menu"] = file1
        file1.add_command(
            label="Display Stratigraphic diagram in phases", command=lambda: self.phasing(), font="helvetica 11"
        )
        self.view_menubar.place(relx=0.07, rely=0, relwidth=0.1, relheight=0.03)

        self.tool_menubar = ttk.Menubutton(self, text="Tools")
        # Adding File Menu and commands
        file2 = tk.Menu(self.tool_menubar, tearoff=0, bg="white", font=("helvetica", 11))
        self.tool_menubar["menu"] = file2
        # file2.add_separator()
        file2.add_command(
            label="Render chronological graph", command=lambda: self.chronograph_render_wrap(), font="helvetica 12 bold"
        )
        file2.add_command(label="Calibrate model", command=lambda: self.load_mcmc(), font="helvetica 12 bold")
        file2.add_command(
            label="Calibrate multiple projects from project",
            command=lambda: popupWindow8(self, proj_dir),
            font="helvetica 12 bold",
        )
        file2.add_command(
            label="Calibrate node delete variations (alpha)",
            command=lambda: popupWindow9(self, proj_dir),
            font="helvetica 12 bold",
        )
        file2.add_command(
            label="Calibrate important variations (alpha)",
            command=lambda: popupWindow10(self, proj_dir),
            font="helvetica 12 bold",
        )

        # file2.add_separator()
        self.tool_menubar.place(relx=0.14, rely=0, relwidth=0.1, relheight=0.03)
        #############################
        self.behindcanvas = tk.Canvas(self.canvas, bd=0, highlightthickness=0, bg="#33658a")
        self.behindcanvas.place(relx=0.003, rely=0.038, relwidth=0.37, relheight=0.96)
        ############################
        self.behindcanvas2 = tk.Canvas(self.canvas, bd=0, highlightthickness=0, bg="#33658a")
        self.behindcanvas2.place(relx=0.38, rely=0.038, relwidth=0.37, relheight=0.96)
        ######################
        self.labelcanvas = tk.Canvas(self.canvas, bd=0, highlightthickness=0, bg="#33658a")
        self.labelcanvas.place(relx=0.003, rely=0.011, relwidth=0.18, relheight=0.027)
        self.labelcanvas1_id = self.labelcanvas.create_text(10, 3, anchor="nw", fill="white")
        self.labelcanvas.itemconfig(self.labelcanvas1_id, text="Stratigraphic graph", font="helvetica 12 bold")
        #########################
        self.littlecanvas = tk.Canvas(
            self.behindcanvas, bd=0, bg="white", selectborderwidth=0, highlightthickness=0, insertwidth=0
        )
        self.littlecanvas_id = self.littlecanvas.create_text(10, 10, anchor="nw", fill="#2f4845")
        self.littlecanvas.place(relx=0.005, rely=0.005, relwidth=0.99, relheight=0.99)
        self.littlecanvas.itemconfig(
            self.littlecanvas_id,
            text="No stratigraphic graph loaded. \n \n \nTo load, go to File > Load stratigraphic diagram",
            font="helvetica 12 bold",
        )
        self.littlecanvas.update()
        ##############################

        #################
        self.littlecanvas2 = tk.Canvas(
            self.behindcanvas2, bd=0, bg="white", selectborderwidth=0, highlightthickness=0, insertwidth=0
        )
        self.littlecanvas2_id = self.littlecanvas2.create_text(10, 10, anchor="nw", fill="#2f4845")
        self.littlecanvas2.itemconfig(
            self.littlecanvas2_id,
            text="No chronological graph loaded. \n \n \nYou must load a stratigraphic graph first. \nTo load, go to File > Load stratigraphic diagram \nTo load your chronological graph, go to Tools > Render chronological graph",
            font="helvetica 12 bold",
        )
        self.littlecanvas2.place(relx=0.005, rely=0.005, relwidth=0.99, relheight=0.99)
        ##########################
        self.labelcanvas2 = tk.Canvas(self.canvas, bd=0, highlightthickness=0, bg="#33658a")
        self.labelcanvas2.place(relx=0.38, rely=0.011, relwidth=0.18, relheight=0.027)
        self.labelcanvas2_id = self.labelcanvas2.create_text(10, 3, anchor="nw", fill="white")
        self.labelcanvas2.itemconfig(self.labelcanvas2_id, text="Chronological graph", font="helvetica 12 bold")
        ###################
        self.littlecanvas.bind("<MouseWheel>", self.wheel)
        self.littlecanvas.bind("<Button-4>", self.wheel)  # only with Linux, wheel scroll down
        self.littlecanvas.bind("<Button-5>", self.wheel)
        self.littlecanvas.bind("<Button-1>", self.move_from)
        self.littlecanvas.bind("<B1-Motion>", self.move_to)

        self.littlecanvas2.bind("<MouseWheel>", self.wheel2)
        self.littlecanvas2.bind("<Button-4>", self.wheel2)  # only with Linux, wheel scroll down
        self.littlecanvas2.bind("<Button-5>", self.wheel2)
        self.littlecanvas2.bind("<Button-1>", self.move_from2)
        self.littlecanvas2.bind("<B1-Motion>", self.move_to2)
        # placing image on littlecanvas from graph
        self.littlecanvas.rowconfigure(0, weight=1)
        self.littlecanvas.columnconfigure(0, weight=1)
        self.littlecanvas2.rowconfigure(0, weight=1)
        self.littlecanvas2.columnconfigure(0, weight=1)
        self.littlecanvas2.update()

        ######node delete##########
        self.OptionList = [
            "Delete context",
            "Delete stratigraphic relationship",
            "Get supplementary data for this context",
            "Equate context with another",
            "Place above other context",
            "Add new contexts",
            "Supplementary data menu (BROKEN)",
        ]
        self.variable = tk.StringVar(self.littlecanvas)
        self.variable.set("Node Action")
        self.testmenu = ttk.OptionMenu(
            self.littlecanvas, self.variable, self.OptionList[0], *self.OptionList, command=self.nodes
        )
        # meta data table
        self.labelcanvas3 = tk.Canvas(self.canvas, bd=0, highlightthickness=0, bg="#33658a")
        self.labelcanvas3.place(relx=0.755, rely=0.695, relwidth=0.17, relheight=0.029)
        self.behindcanvas3 = tk.Canvas(self.canvas, bd=0, highlightthickness=0, bg="#33658a")
        self.behindcanvas3.place(relx=0.755, rely=0.719, relwidth=0.23, relheight=0.278)
        self.metatext_id = self.labelcanvas3.create_text(10, 5, anchor="nw", fill="white")
        self.labelcanvas3.itemconfig(self.metatext_id, text="Supplementary data", font="helvetica 12 bold")
        self.tree1 = ttk.Treeview(self.canvas)
        self.tree1["columns"] = ["Data"]
        self.tree1.place(relx=0.758, rely=0.725)
        self.tree1.column("Data", anchor="w")
        self.tree1.heading("Data", text="Data")
        # deleted contexts table
        self.labelcanvas4 = tk.Canvas(self.canvas, bd=0, highlightthickness=0, bg="#33658a")
        self.labelcanvas4.place(relx=0.755, rely=0.04, relwidth=0.17, relheight=0.029)
        self.behindcanvas4 = tk.Canvas(self.canvas, bd=0, highlightthickness=0, bg="#33658a")
        self.behindcanvas4.place(relx=0.755, rely=0.069, relwidth=0.23, relheight=0.278)
        self.delcontext_id = self.labelcanvas4.create_text(10, 5, anchor="nw", fill="white")
        self.labelcanvas4.itemconfig(self.delcontext_id, text="Deleted Contexts", font="helvetica 12 bold")
        self.tree2 = ttk.Treeview(self.canvas)

        self.tree2.heading("#0", text="Context")
        self.tree2["columns"] = ["Meta"]
        self.tree2.place(relx=0.758, rely=0.0729)
        self.tree2.column("Meta", anchor="w")
        self.tree2.heading("Meta", text="Reason for deleting")

        # deleted edges table
        self.labelcanvas5 = tk.Canvas(self.canvas, bd=0, highlightthickness=0, bg="#33658a")
        self.labelcanvas5.place(relx=0.755, rely=0.371, relwidth=0.17, relheight=0.029)
        self.behindcanvas5 = tk.Canvas(self.canvas, bd=0, highlightthickness=0, bg="#33658a")
        self.behindcanvas5.place(relx=0.755, rely=0.399, relwidth=0.23, relheight=0.278)
        self.deledge_id = self.labelcanvas5.create_text(10, 5, anchor="nw", fill="white")
        self.labelcanvas5.itemconfig(
            self.deledge_id, text="Deleted Stratigraphic Relationships", font="helvetica 12 bold"
        )
        self.tree3 = ttk.Treeview(self.canvas)
        self.tree3.heading("#0", text="Stratigraphic relationship")
        self.tree3["columns"] = ["Meta"]
        self.tree3.place(relx=0.758, rely=0.405)
        self.tree3.heading("Meta", text="Reason for deleting")
        f = dir(self)
        self.f_1 = [var for var in f if ("__" or "grid" or "get") not in var]
        self.littlecanvas.update()
        try:
            self.restore_state()
        except FileNotFoundError:
            self.save_state_1()
        self.databutton = tk.Button(
            self,
            text="Data loaded  ↙",
            font="helvetica 12 bold",
            fg="white",
            command=lambda: self.display_data_func(),
            bd=0,
            highlightthickness=0,
            bg="#33658a",
        )
        self.databutton.place(relx=0.303, rely=0.04, relwidth=0.07, relheight=0.028)
        self.datacanvas = tk.Canvas(self.behindcanvas, bd=0, highlightthickness=0, bg="#33658a")
        self.datacanvas.place(relx=0.55, rely=0.0, relwidth=0.45, relheight=0.2)
        self.datalittlecanvas = tk.Canvas(
            self.datacanvas, bd=8, bg="white", highlightbackground="#33658a", highlightthickness=5
        )
        self.datalittlecanvas.place(relx=0.015, rely=0.015, relwidth=0.97, relheight=0.97)
        self.display_data_var = "hidden"
        self.check_list_gen()
        tk.Misc.lift(self.littlecanvas)

    def refresh_4_new_model(self, controller, proj_dir, load):
        extra_top = load_Window.new_model(load_Window(MAIN_FRAME), proj_dir, load)
        self.wait_window(extra_top)

    #       self.save_state_1()

    def display_data_func(self):
        if self.display_data_var == "hidden":
            tk.Misc.lift(self.datacanvas)
            self.databutton["text"] = "Data loaded ↗"
            self.display_data_var = "onshow"
        else:
            if self.display_data_var == "onshow":
                tk.Misc.lift(self.littlecanvas)
                self.databutton["text"] = "Data loaded  ↙"
                self.display_data_var = "hidden"

    def check_list_gen(self):
        if self.strat_check:
            strat = "‣ Stratigraphic relationships"
            col1 = "green"
        else:
            strat = "‣ Stratigraphic relationships"
            col1 = "black"
        if self.date_check:
            date = "‣ Radiocarbon dates"
            col2 = "green"
        else:
            date = "‣ Radiocarbon dates"
            col2 = "black"
        if self.phase_check:
            phase = "‣ Groups for contexts"
            col3 = "green"
        else:
            phase = "‣ Groups for contexts"
            col3 = "black"
        if self.phase_rel_check:
            rels = "‣ Relationships between groups"
            col4 = "green"
        else:
            rels = "‣ Relationships between groups"
            col4 = "black"
        self.datalittlecanvas.delete("all")
        self.datalittlecanvas.create_text(
            10, 20, anchor="nw", text=strat + "\n\n", font=("Helvetica 12 bold"), fill=col1
        )
        self.datalittlecanvas.pack()
        self.datalittlecanvas.create_text(
            10, 50, anchor="nw", text=date + "\n\n", font=("Helvetica 12 bold"), fill=col2
        )
        self.datalittlecanvas.pack()
        self.datalittlecanvas.create_text(
            10, 80, anchor="nw", text=phase + "\n\n", font=("Helvetica 12 bold"), fill=col3
        )
        self.datalittlecanvas.pack()
        self.datalittlecanvas.create_text(10, 110, anchor="nw", text=rels, font=("Helvetica 12 bold"), fill=col4)
        self.datalittlecanvas.pack()

    def destroy1(self):
        """destroys self.testmenu"""
        self.menubar.place_forget()

    def resid_check(self):
        """Loads a text box to check if the user thinks any samples are residual"""
        global load_check
        MsgBox = tk.messagebox.askquestion(
            "Residual and Intrusive Contexts",
            "Do you suspect any of your samples are residual or intrusive?",
            icon="warning",
        )
        if MsgBox == "yes":
            pagetwo = PageTwo(self, self.controller)
            self.popup3 = pagetwo.popup4

        else:
            self.popup3 = popupWindow3(self, self.graph, self.littlecanvas2, self.phase_rels)

        def destroy(self):
            """destroys self.testmenu"""
            self.testmenu.place_forget()

        #    # This is the function that removes the selected item when the label is clicked.
        def delete(self, *args):
            """uses destroy then sets self.variable"""
            self.destroy()
            self.testmenu.place_forget()
            self.variable.set("Node Action")

    def save_state_1(self):
        global mcmc_check, load_check, FILE_INPUT
        # converting metadata treeview to dataframe
        row_list = []
        columns = ("context", "Reason for deleting")
        for child in self.tree2.get_children():
            row_list.append((self.tree2.item(child)["text"], self.tree2.item(child)["values"]))
        self.treeview_df = pd.DataFrame(row_list, columns=columns)
        vars_list_1 = dir(self)
        #      self.node_importance(self.graph)
        var_list = [
            var
            for var in vars_list_1
            if (("__" and "grid" and "get" and "tkinter" and "children") not in var) and (var[0] != "_")
        ]
        data = {}
        # Type names to not pickle when saving state. PolyChron is excluded to avoid classes which inherit from tk, this may be a bit too strong.
        check_list = ["tkinter", "method", "__main__", "PIL", "PolyChron"]

        for i in var_list:
            v = getattr(self, i)
            if not any(x in str(type(v)) for x in check_list):
                data[i] = v
        data["all_vars"] = list(data.keys())
        data["load_check"] = load_check
        data["mcmc_check"] = mcmc_check
        data["file_input"] = FILE_INPUT
        if mcmc_check == "mcmc_loaded":
            results = data["all_results_dict"]
            df = pd.DataFrame()
            for i in results.keys():
                df[i] = results[i][10000:]
            results_path = os.getcwd() + "/mcmc_results/full_results_df"
            df.to_csv(results_path)
            phasefile = data["phasefile"]
            context_no = data["CONTEXT_NO"]
            key_ref = [list(phasefile["Group"])[list(phasefile["context"]).index(i)] for i in context_no]
            df1 = pd.DataFrame(key_ref)
            df1.to_csv("mcmc_results/key_ref.csv")
            df2 = pd.DataFrame(context_no)
            df2.to_csv("mcmc_results/context_no.csv")
        path = os.getcwd() + "/python_only/save.pickle"
        path2 = os.getcwd() + "/stratigraphic_graph/deleted_contexts_meta"
        self.treeview_df.to_csv(path2)
        try:
            with open(path, "wb") as f:
                pickle.dump(data, f)
        except Exception as e:
            print("error saving state:", str(e))

    def restore_state(self):
        global mcmc_check, load_check, FILE_INPUT
        with open("python_only/save.pickle", "rb") as f:
            data = pickle.load(f)
            vars_list = data["all_vars"]
            for i in vars_list:
                setattr(self, i, data[i])
            FILE_INPUT = data["file_input"]
            load_check = data["load_check"]
            mcmc_check = data["mcmc_check"]
        if self.graph is not None:
            self.littlecanvas.delete("all")
            self.rerender_stratdag()
            for i, j in enumerate(self.treeview_df["context"]):
                self.tree2.insert("", "end", text=j, values=self.treeview_df["Reason for deleting"][i])

        if load_check == "loaded":
            FILE_INPUT = None
            # manaually work this out as canvas hasn't rendered enough at this point to have a height and width in pixels
            height = 0.96 * 0.99 * 0.97 * 1000 * 0.96
            width = 0.99 * 0.37 * 2000 * 0.96
            self.image2 = imgrender2(width, height)
            if self.image2 != "No_image":
                self.littlecanvas2.delete("all")
                self.littlecanvas2.img = ImageTk.PhotoImage(self.image2)
                self.littlecanvas2_img = self.littlecanvas2.create_image(
                    0, 0, anchor="nw", image=self.littlecanvas2.img
                )

                self.width2, self.height2 = self.image2.size
                #  self.imscale2 = 1.0  # scale for the canvaas image
                self.delta2 = 1.1  # zoom magnitude
                # Put image into container rectangle and use it to set proper coordinates to the image
                self.container2 = self.littlecanvas2.create_rectangle(0, 0, self.width2, self.height2, width=0)
                self.imscale2 = min(921 / self.image2.size[0], 702 / self.image2.size[1])
                self.littlecanvas.scale("all", 0, 0, self.delta2, self.delta2)  # rescale all canvas objects
                self.show_image2()

                self.littlecanvas2.bind("<Configure>", self.resize2)

    def onRight(self, *args):
        """makes test menu appear after right click"""
        self.littlecanvas.unbind("Button-1>")
        self.littlecanvas.bind("<Button-1>", self.onLeft)
        # Here we fetch our X and Y coordinates of the cursor RELATIVE to the window
        self.cursorx = int(self.littlecanvas.winfo_pointerx() - self.littlecanvas.winfo_rootx())
        self.cursory = int(self.littlecanvas.winfo_pointery() - self.littlecanvas.winfo_rooty())
        if self.image != "noimage":
            x_scal = self.cursorx + self.transx
            y_scal = self.cursory + self.transy
            self.node = self.nodecheck(x_scal, y_scal)
        # Now we define our right click menu canvas
        # And here is where we use our X and Y variables, to place the menu where our cursor is,
        # That's how right click menus should be placed.
        self.testmenu.place(x=self.cursorx, y=self.cursory)
        # This is for packing our options onto the canvas, to prevent the canvas from resizing.
        # This is extremely useful if you split your program into multiple canvases or frames
        # and the pack method is forcing them to resize.
        self.testmenu.pack_propagate(0)
        # Here is our label on the right click menu for deleting a row, notice the cursor
        # value, which will give us a pointy finger when you hover over the option.
        self.testmenuWidth = len(max(self.OptionList, key=len))
        self.testmenu.config(width=self.testmenuWidth)
        # This function is for removing the canvas when an option is clicked.

    def preClick(self, *args):
        """makes test menu appear and removes any previous test menu"""
        try:
            self.testmenu.place_forget()
            self.onRight()
        except Exception:
            self.onRight()

    # Hide menu when left clicking
    def onLeft(self, *args):
        """hides menu when left clicking"""
        try:
            self.testmenu.place_forget()
        except Exception:
            pass

    def file_popup(self, file):
        self.nodedel = popupWindow7(self.canvas, file)
        self.canvas["state"] = "disabled"
        self.master.wait_window(self.nodedel.top)
        self.canvas["state"] = "normal"
        return self.nodedel.value

    def open_file1(self):
        """opens dot file"""
        global node_df, FILE_INPUT, phase_true
        file = askopenfile(mode="r", filetypes=[("Python Files", "*.dot")])
        FILE_INPUT = file.name
        self.graph = nx.DiGraph(imagefunc(file.name), graph_attr={"splines": "ortho"})
        if phase_true == 1:
            self.image = imgrender_phase(self.graph)
        else:
            self.image = imgrender(self.graph)
        self.littlecanvas.img = ImageTk.PhotoImage(self.image)
        self.littlecanvas_img = self.littlecanvas.create_image(0, 0, anchor="nw", image=self.littlecanvas.img)

        self.width, self.height = self.image.size
        self.imscale = 1.0  # scale for the canvaas image
        #  self.imscale  = min(921/self.image.size[0], 702/self.image.size[1])
        self.delta = 1.1  # zoom magnitude
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.littlecanvas.create_rectangle(0, 0, self.width, self.height, width=0)
        self.bind("<Configure>", self.resize)
        self.littlecanvas.scale("all", 0, 0, self.delta, self.delta)  # rescale all canvas objects
        self.show_image()
        self.littlecanvas.bind("<Configure>", self.resize)
        self.delnodes = []
        self.delnodes_meta = []
        self.canvas.delete("all")
        self.littlecanvas.bind("<Button-3>", self.preClick)

    def rerender_stratdag(self):
        global phase_true
        """rerenders stratdag after reloading previous project"""
        height = 0.96 * 0.99 * 0.97 * 1000
        width = 0.99 * 0.37 * 2000 * 0.96
        if phase_true == 1:
            self.image = imgrender_phase(self.graph)
        else:
            self.image = imgrender(self.graph, width, height)

        #       self.image = self.image_ws.resize((int(self.image_ws.size[0]*scale_factor), int(self.image_ws.size[1]*scale_factor)), Image.ANTIALIAS)
        self.littlecanvas.img = ImageTk.PhotoImage(self.image)
        self.littlecanvas_img = self.littlecanvas.create_image(0, 0, anchor="nw", image=self.littlecanvas.img)

        self.width, self.height = self.image.size
        #   self.imscale = 1.0  # scale for the canvaas image
        self.delta = 1.1  # zoom magnitude
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.littlecanvas.create_rectangle(0, 0, self.width, self.height, width=0)
        self.imscale = min(width / self.image.size[0], height / self.image.size[1])

        self.delnodes = []
        self.delnodes_meta = []
        self.littlecanvas.bind("<Button-3>", self.preClick)
        self.littlecanvas.update()
        self.littlecanvas.scale("all", 0, 0, self.delta, self.delta)  # rescale all canvas objects
        self.show_image()

    def chronograph_render_wrap(self):
        """wraps chronograph render so we can assign a variable when runing the func using a button"""
        global load_check
        if (self.phase_rels is None) or (self.phasefile is None) or (self.datefile is None):
            tk.messagebox.showinfo("Error", "You haven't loaded in all the data required for a chronological graph")
        if load_check == "loaded":
            answer = askquestion(
                "Warning!",
                "Chronological DAG already loaded, are you sure you want to write over it? You can copy this model in the file menu if you want to consider multiple models",
            )
            if answer == "yes":
                self.refresh_4_new_model(self.controller, proj_dir, load=False)
                load_check = "not_loaded"
                self.littlecanvas2.delete("all")
                self.chrono_dag = self.chronograph_render()
                startpage = self.controller.get_page("StartPage")
                startpage.CONT_TYPE = self.popup3.CONT_TYPE
                startpage.prev_phase = self.popup3.prev_phase
                startpage.post_phase = self.popup3.post_phase
                startpage.phi_ref = self.popup3.phi_ref
                startpage.context_no_unordered = self.popup3.context_no_unordered
                startpage.graphcopy = self.popup3.graphcopy
                startpage.node_del_tracker = self.popup3.node_del_tracker

        else:
            self.littlecanvas2.delete("all")
            self.chrono_dag = self.chronograph_render()
            startpage = self.controller.get_page("StartPage")
            startpage.CONT_TYPE = self.popup3.CONT_TYPE
            startpage.prev_phase = self.popup3.prev_phase
            startpage.post_phase = self.popup3.post_phase
            startpage.phi_ref = self.popup3.phi_ref
            startpage.context_no_unordered = self.popup3.context_no_unordered
            startpage.graphcopy = self.popup3.graphcopy
            startpage.node_del_tracker = self.popup3.node_del_tracker

    def open_file2(self):
        """opens plain text strat file"""
        global FILE_INPUT, phase_true
        file = askopenfile(mode="r", filetypes=[("Python Files", "*.csv")])
        if file is not None:
            try:
                FILE_INPUT = None
                self.littlecanvas.delete("all")
                self.stratfile = pd.read_csv(file, dtype=str)
                load_it = self.file_popup(self.stratfile)
                if load_it == "load":
                    self.strat_check = True
                    G = nx.DiGraph(graph_attr={"splines": "ortho"})
                    set1 = set(self.stratfile.iloc[:, 0])
                    set2 = set(self.stratfile.iloc[:, 1])
                    set2.update(set1)
                    node_set = {x for x in set2 if x == x}
                    for i in set(node_set):
                        G.add_node(i, shape="box", fontname="helvetica", fontsize="30.0", penwidth="1.0", color="black")
                        G.nodes()[i].update({"Determination": [None, None]})
                        G.nodes()[i].update({"Group": None})
                    edges = []
                    for i in range(len(self.stratfile)):
                        a = tuple(self.stratfile.iloc[i, :])
                        if not pd.isna(a[1]):
                            edges.append(a)
                    G.add_edges_from(edges, arrowhead="none")
                    self.graph = G
                    if phase_true == 1:
                        self.image = imgrender_phase(self.graph)
                    else:
                        self.image = imgrender(
                            self.graph, self.littlecanvas.winfo_width(), self.littlecanvas.winfo_height()
                        )

                        #     scale_factor = min(self.littlecanvas.winfo_width()/self.image_ws.size[0], self.littlecanvas.winfo_height()/self.image_ws.size[1])
                        #     self.image = self.image_ws.resize((int(self.image_ws.size[0]*scale_factor), int(self.image_ws.size[1]*scale_factor)), Image.ANTIALIAS)
                        self.littlecanvas.img = ImageTk.PhotoImage(self.image)
                        self.littlecanvas_img = self.littlecanvas.create_image(
                            0, 0, anchor="nw", image=self.littlecanvas.img
                        )
                        self.width, self.height = self.image.size
                        #     self.imscale = 1.0#, self.littlecanvas.winfo_height()/self.image.size[1])# scale for the canvaas image
                        self.delta = 1.1  # zoom magnitude
                        # Put image into container rectangle and use it to set proper coordinates to the image
                        self.container = self.littlecanvas.create_rectangle(0, 0, self.width, self.height, width=0)
                        self.bind("<Configure>", self.resize)
                        self.littlecanvas.bind("<Configure>", self.resize)
                        self.delnodes = []
                        self.delnodes_meta = []
                        self.littlecanvas.bind("<Button-3>", self.preClick)
                        self.imscale = min(921 / self.image.size[0], 702 / self.image.size[1])
                        self.littlecanvas.scale("all", 0, 0, self.delta, self.delta)  # rescale all canvas objects
                        self.show_image()
                    tk.messagebox.showinfo("Success", "Stratigraphic data loaded")
                    self.check_list_gen()
            except ValueError:
                tk.messagebox.showerror("showerror", "Data not loaded, please try again")

    def open_file3(self):
        """opens scientific dating file"""
        file = askopenfile(mode="r", filetypes=[("Python Files", "*.csv")])
        if file is not None:
            try:
                self.datefile = pd.read_csv(file)
                self.datefile = self.datefile.applymap(str)
                load_it = self.file_popup(self.datefile)
                if load_it == "load":
                    for i, j in enumerate(self.datefile["context"]):
                        self.graph.nodes()[str(j)].update(
                            {"Determination": [self.datefile["date"][i], self.datefile["error"][i]]}
                        )
                    self.context_no_unordered = list(self.graph.nodes())
                self.date_check = True
                self.check_list_gen()
                tk.messagebox.showinfo("Success", "Scientific dating data loaded")
            except ValueError:
                tk.messagebox.showerror("showerror", "Data not loaded, please try again")

    def open_file4(self):
        """opens phase file"""
        file = askopenfile(mode="r", filetypes=[("Pythotransxn Files", "*.csv")])
        if file is not None:
            try:
                self.phasefile = pd.read_csv(file)
                self.phasefile = self.phasefile.applymap(str)
                load_it = self.file_popup(self.phasefile)
                if load_it == "load":
                    for i, j in enumerate(self.phasefile["context"]):
                        self.graph.nodes()[str(j)].update({"Group": self.phasefile["Group"][i]})
                self.phase_check = True
                self.check_list_gen()
                tk.messagebox.showinfo("Success", "Grouping data loaded")
            except ValueError:
                tk.messagebox.showerror("showerror", "Data not loaded, please try again")

    def open_file5(self):
        """opens phase relationship files"""
        file = askopenfile(mode="r", filetypes=[("Python Files", "*.csv")])
        if file is not None:
            try:
                phase_rel_df = pd.read_csv(file)
                self.phase_rels = [
                    (str(phase_rel_df["above"][i]), str(phase_rel_df["below"][i])) for i in range(len(phase_rel_df))
                ]
                self.file_popup(pd.DataFrame(self.phase_rels, columns=["Younger group", "Older group"]))
                self.phase_rel_check = True
                self.check_list_gen()
                tk.messagebox.showinfo("Success", "Group relationships data loaded")
            except ValueError:
                tk.messagebox.showerror("showerror", "Data not loaded, please try again")

    def open_file6(self):
        """opens files determining equal contexts (in time)"""
        global phase_true
        file = askopenfile(mode="r", filetypes=[("Python Files", "*.csv")])
        if file is not None:
            try:
                equal_rel_df = pd.read_csv(file)
                self.equal_rel_df = equal_rel_df.applymap(str)
                context_1 = list(self.equal_rel_df.iloc[:, 0])
                context_2 = list(self.equal_rel_df.iloc[:, 1])
                for k, j in enumerate(context_1):
                    self.graph = nx.contracted_nodes(self.graph, j, context_2[k])
                    x_nod = list(self.graph)
                    newnode = str(j) + " = " + str(context_2[k])
                    y_nod = [newnode if i == j else i for i in x_nod]
                    mapping = dict(zip(x_nod, y_nod))
                    self.graph = nx.relabel_nodes(self.graph, mapping)
                if phase_true == 1:
                    imgrender_phase(self.graph)
                else:
                    imgrender(self.graph, self.littlecanvas.winfo_width(), self.littlecanvas.winfo_height())
                self.image = Image.open("testdag.png")
                #   scale_factor = min(self.littlecanvas.winfo_width()/self.image_ws.size[0], self.littlecanvas.winfo_height()/self.image_ws.size[1])
                #   self.image = self.image_ws.resize((int(self.image_ws.size[0]*scale_factor), int(self.image_ws.size[1]*scale_factor)), Image.ANTIALIAS)
                self.width, self.height = self.image.size
                self.container = self.littlecanvas.create_rectangle(0, 0, self.width, self.height, width=0)
                self.show_image()
                tk.messagebox.showinfo("Success", "Equal contexts data loaded")
            except ValueError:
                tk.messagebox.showerror("showerror", "Data not loaded, please try again")

    def cleanup(self):
        """destroys mcmc loading page when done"""
        self.top.destroy()

    def load_mcmc(self):
        """loads mcmc loading page"""
        global mcmc_check
        self.top = tk.Toplevel(self.littlecanvas)
        self.backcanvas = tk.Canvas(self.top, bg="#AEC7D6")
        self.backcanvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.top.geometry("%dx%d%+d%+d" % (700, 200, 600, 400))
        self.l = tk.Label(
            self.backcanvas, text="MCMC in progress", font=("helvetica 14 bold"), fg="#2F4858", bg="#AEC7D6"
        )
        self.l.place(relx=0.35, rely=0.26)
        outputPanel = tk.Label(self.backcanvas, font=("helvetica 14 bold"), fg="#2F4858", bg="#AEC7D6")
        outputPanel.place(relx=0.4, rely=0.4)
        pb1 = ttk.Progressbar(self.backcanvas, orient=tk.HORIZONTAL, length=400, mode="indeterminate")
        pb1.place(relx=0.2, rely=0.56)
        old_stdout = sys.stdout
        sys.stdout = StdoutRedirector(outputPanel, pb1)
        self.ACCEPT = [[]]
        while min([len(i) for i in self.ACCEPT]) < 50000:
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
            ) = self.MCMC_func()
        mcmc_check = "mcmc_loaded"
        sys.stdout = old_stdout
        self.controller.show_frame("PageOne")
        f = dir(self)
        self.f_2 = [var for var in f if ("__" or "grid" or "get") not in var]
        self.newvars = [var for var in self.f_2 if var not in self.f_1]
        self.cleanup()

    def addedge(self, edgevec):
        """adds an edge relationship (edgevec) to graph and rerenders the graph"""
        global node_df, phase_true
        x_1 = edgevec[0]
        x_2 = edgevec[1]
        self.graph.add_edge(x_1, x_2, arrowhead="none")
        self.graph_check = nx.transitive_reduction(self.graph)
        if self.graph.edges() != self.graph_check.edges():
            self.graph.remove_edge(x_1, x_2)
            tk.messagebox.showerror(
                "Redundant relationship",
                "That stratigraphic relationship is already implied by other relationships in the graph",
            )
        if phase_true == 1:
            imgrender_phase(self.graph)
        else:
            imgrender(self.graph, self.littlecanvas.winfo_width(), self.littlecanvas.winfo_height())
        self.image = Image.open("testdag.png")
        self.show_image()

    def chronograph_render(self):
        """initiates residual checking function then renders the graph when thats done"""
        global load_check
        if load_check != "loaded":
            load_check = "loaded"
            self.resid_check()
            self.image2 = imgrender2(self.littlecanvas2.winfo_width(), self.littlecanvas2.winfo_height())
            if self.image2 != "No_image":
                try:
                    self.littlecanvas2.delete("all")
                    self.littlecanvas2.img = ImageTk.PhotoImage(self.image2)
                    self.littlecanvas2_img = self.littlecanvas2.create_image(
                        0, 0, anchor="nw", image=self.littlecanvas2.img
                    )

                    self.width2, self.height2 = self.image2.size
                    # self.imscale2 = 1.0  # scale for the canvaas image
                    self.delta2 = 1.1  # zoom magnitude
                    # Put image into container rectangle and use it to set proper coordinates to the image
                    self.container2 = self.littlecanvas2.create_rectangle(0, 0, self.width2, self.height2, width=0)
                    self.imscale2 = min(921 / self.image2.size[0], 702 / self.image2.size[1])
                    self.littlecanvas2.scale("all", 0, 0, self.delta2, self.delta2)  # rescale all canvas objects
                    self.show_image2()
                    self.littlecanvas2.bind("<Configure>", self.resize2)
                except (RuntimeError, TypeError, NameError):
                    load_check = "not_loaded"
        return self.popup3.graphcopy

    def stratfunc(self, node):
        """obtains strat relationships for node"""
        rellist = list(nx.line_graph(self.graph))
        above = ()
        below = ()
        for i in enumerate(rellist):
            if str(node) in rellist[i[0]]:
                if str(node) == rellist[i[0]][0]:
                    below = np.append(below, rellist[i[0]][1])
                elif str(node) == rellist[i[0]][1]:
                    above = np.append(above, rellist[i[0]][0])
        if len(above) == 0:
            str1 = ""
        else:
            str1 = above[0]
            for i in above[1:]:
                str1 = str1 + ", " + i
        if len(below) == 0:
            str2 = ""
        else:
            str2 = below[0]
            for j in below[1:]:
                str2 = str2 + ", " + j
        return [str1, str2]

    def MCMC_func(self):
        """gathers all the inputs for the mcmc module and then runs it and returns resuslts dictionaries"""
        context_no = [x for x in list(self.context_no_unordered) if x not in self.node_del_tracker]
        TOPO = list(nx.topological_sort(self.chrono_dag))
        self.TOPO_SORT = [x for x in TOPO if (x not in self.node_del_tracker) and (x in context_no)]
        self.TOPO_SORT.reverse()
        context_no = self.TOPO_SORT
        self.key_ref = [list(self.phasefile["Group"])[list(self.phasefile["context"]).index(i)] for i in context_no]
        self.CONT_TYPE = [self.CONT_TYPE[list(self.context_no_unordered).index(i)] for i in self.TOPO_SORT]
        strat_vec = []
        resids = [j for i, j in enumerate(context_no) if self.CONT_TYPE[i] == "residual"]
        intrus = [j for i, j in enumerate(context_no) if self.CONT_TYPE[i] == "intrusive"]
        for i, j in enumerate(context_no):
            if self.CONT_TYPE[i] == "residual":
                low = []
                up = list(self.graph.predecessors(j))
            elif self.CONT_TYPE[i] == "intrusive":
                low = list(self.graph.successors(j))
                up = []
            else:
                up = [k for k in self.graph.predecessors(j) if k not in resids]
                low = [k for k in self.graph.successors(j) if k not in intrus]
            strat_vec.append([up, low])
        # strat_vec = [[list(self.graph.predecessors(i)), list(self.graph.successors(i))] for i in context_no]
        self.RCD_EST = [int(list(self.datefile["date"])[list(self.datefile["context"]).index(i)]) for i in context_no]
        self.RCD_ERR = [int(list(self.datefile["error"])[list(self.datefile["context"]).index(i)]) for i in context_no]
        rcd_est = self.RCD_EST
        rcd_err = self.RCD_ERR
        self.prev_phase, self.post_phase = self.prev_phase, self.post_phase
        input_1 = [
            strat_vec,
            rcd_est,
            rcd_err,
            self.key_ref,
            context_no,
            self.phi_ref,
            self.prev_phase,
            self.post_phase,
            self.TOPO_SORT,
            self.CONT_TYPE,
        ]
        f = open("input_file", "w")
        writer = csv.writer(f)
        #  for i in input_1:
        writer.writerow(input_1)
        f.close()
        CONTEXT_NO, ACCEPT, PHI_ACCEPT, PHI_REF, A, P, ALL_SAMPS_CONT, ALL_SAMPS_PHI = mcmc.run_MCMC(
            CALIBRATION,
            strat_vec,
            rcd_est,
            rcd_err,
            self.key_ref,
            context_no,
            self.phi_ref,
            self.prev_phase,
            self.post_phase,
            self.TOPO_SORT,
            self.CONT_TYPE,
        )
        phase_nodes, resultsdict, all_results_dict = phase_labels(PHI_REF, self.post_phase, PHI_ACCEPT, ALL_SAMPS_PHI)
        for i, j in enumerate(CONTEXT_NO):
            resultsdict[j] = ACCEPT[i]
        for k, l in enumerate(CONTEXT_NO):
            all_results_dict[l] = ALL_SAMPS_CONT[k]

        return (
            CONTEXT_NO,
            ACCEPT,
            PHI_ACCEPT,
            PHI_REF,
            A,
            P,
            ALL_SAMPS_CONT,
            ALL_SAMPS_PHI,
            resultsdict,
            all_results_dict,
        )

    def nodecheck(self, x_current, y_current):
        """returns the node that corresponds to the mouse cooridinates"""
        node_inside = "no node"
        if phase_true == 1:
            (graph,) = pydot.graph_from_dot_file("fi_new.txt")
            node_df_con = node_coords_fromjson(graph)
        else:
            node_df_con = node_coords_fromjson(self.graph)
        node_df = node_df_con[0]

        xmax, ymax = node_df_con[1]
        # forms a dataframe from the dicitonary of coords
        x, y = self.image.size
        cavx = x * self.imscale
        cany = y * self.imscale
        xscale = (x_current) * (xmax) / cavx
        yscale = (cany - y_current) * (ymax) / cany
        for n_ind in range(node_df.shape[0]):
            if (node_df.iloc[n_ind].x_lower < xscale < node_df.iloc[n_ind].x_upper) and (
                node_df.iloc[n_ind].y_lower < yscale < node_df.iloc[n_ind].y_upper
            ):
                node_inside = node_df.iloc[n_ind].name
                self.graph[node_inside]
        return node_inside

    def edge_render(self):
        """renders string for deleted edges"""
        self.edges_del = self.edge_nodes
        ednodes = str(self.edges_del[0]) + " above " + str(self.edges_del[1])
        self.temp = str(self.temp).replace("[", "")
        self.temp = str(self.temp).replace("]", "")
        self.temp = self.temp + str(ednodes.replace("'", ""))

    def node_del_popup(self):
        self.nodedel = popupWindow5(self.canvas)
        self.canvas["state"] = "disabled"
        self.master.wait_window(self.nodedel.top)
        self.canvas["state"] = "normal"
        return self.nodedel.value

    def edge_del_popup(self):
        self.nodedel = popupWindow6(self.canvas)
        self.canvas["state"] = "disabled"
        self.master.wait_window(self.nodedel.top)
        self.canvas["state"] = "normal"
        return self.nodedel.value

    def nodes(self, currentevent):
        """performs action using the node and redraws the graph"""
        global load_check, phase_true
        self.testmenu.place_forget()
        # deleting a single context
        if self.variable.get() == "Delete context":
            if self.node != "no node":
                if load_check == "loaded":
                    load_check = "not_loaded"
                    answer = askquestion(
                        "Warning!",
                        "Chronological DAG already loaded, do you want to save this as a new model first? \n\n Click Yes to save as new model and No to overwrite existing model",
                    )
                    if answer == "yes":
                        self.refresh_4_new_model(self.controller, proj_dir, load=False)
                    self.littlecanvas2.delete("all")
                #   self.graph.remove_node(self.node)
                self.graph = node_del_fixed(self.graph, self.node)
                self.nodedel_meta = self.node_del_popup()
                self.delnodes = np.append(self.delnodes, self.node)
                self.delnodes_meta.append(self.nodedel_meta)
                self.tree2.insert("", "end", text=self.node, values=[self.nodedel_meta])
        # presents popup list to label new context
        if self.variable.get() == "Add new contexts":
            if load_check == "loaded":
                answer = askquestion(
                    "Warning!",
                    "Chronological DAG already loaded, do you want to save this as a new model first? \n Click YES to save as new model and NO to overwrite existing model",
                )
                if answer == "yes":
                    self.refresh_4_new_model(self.controller, proj_dir, load=False)
                self.littlecanvas2.delete("all")
                load_check = "not_loaded"
            self.w = popupWindow(self)
            self.wait_window(self.w.top)
            self.node = self.w.value
            self.graph.add_node(self.node, shape="box", fontsize="30.0", fontname="helvetica", penwidth="1.0")
        # checks if any nodes are in edge node to see if we want to add/delete a context
        if len(self.edge_nodes) == 1:
            # first case deletes strat relationships
            if self.variable.get() == "Delete stratigraphic relationship with " + str(self.edge_nodes[0]):
                self.edge_nodes = np.append(self.edge_nodes, self.node)
                self.reason = self.edge_del_popup()
                if load_check == "loaded":
                    answer = askquestion(
                        "Warning!",
                        "Chronological DAG already loaded, do you want to save this as a new model first? \n Click YES to save as new model and NO to overwrite existing model",
                    )
                    if answer == "yes":
                        self.refresh_4_new_model(self.controller, proj_dir, load=False)
                    self.littlecanvas2.delete("all")
                    load_check = "not_loaded"
                try:
                    self.graph.remove_edge(self.edge_nodes[0], self.edge_nodes[1])
                    self.edge_render()
                    self.tree3.insert("", 0, text=self.temp, values=self.reason)
                    self.tree3.update()
                except (KeyError, nx.exception.NetworkXError):
                    try:
                        self.graph.remove_edge(self.edge_nodes[1], self.edge_nodes[0])
                        self.edge_render()
                    except (KeyError, nx.exception.NetworkXError):
                        tk.messagebox.showinfo("Error", "An edge doesnt exist between those nodes")

                self.OptionList.remove("Delete stratigraphic relationship with " + str(self.edge_nodes[0]))
                self.testmenu = ttk.OptionMenu(
                    self.littlecanvas, self.variable, self.OptionList[0], *self.OptionList, command=self.nodes
                )
                self.edge_nodes = []
            # second case is adding a strat relationship
            elif self.variable.get() == ("Place " + str(self.edge_nodes[0]) + " Above"):
                if load_check == "loaded":
                    answer = askquestion(
                        "Warning!",
                        "Chronological DAG already loaded, do you want to save this as a new model first? \n Click YES to save as new model and NO to overwrite existing model",
                    )
                    if answer == "yes":
                        self.refresh_4_new_model(self.controller, proj_dir, load=False)
                self.littlecanvas2.delete("all")
                load_check = "not_loaded"
                self.edge_nodes = np.append(self.edge_nodes, self.node)
                self.addedge(self.edge_nodes)
                self.OptionList.remove("Place " + str(self.edge_nodes[0]) + " Above")
                self.testmenu = ttk.OptionMenu(
                    self.littlecanvas, self.variable, self.OptionList[0], *self.OptionList, command=self.nodes
                )
                self.edge_nodes = []
        # sets up the menu to delete the strat relationship once user picks next node
        if self.variable.get() == "Delete stratigraphic relationship":
            if len(self.edge_nodes) == 1:
                self.OptionList.remove("Delete stratigraphic relationship with " + str(self.edge_nodes[0]))
                self.edge_nodes = []
            self.edge_nodes = np.append(self.edge_nodes, self.node)
            self.OptionList.append("Delete stratigraphic relationship with " + str(self.edge_nodes[0]))
            self.testmenu = ttk.OptionMenu(
                self.littlecanvas, self.variable, self.OptionList[0], *self.OptionList, command=self.nodes
            )
        # equates too contexts
        if len(self.comb_nodes) == 1:
            if self.variable.get() == "Equate context with " + str(self.comb_nodes[0]):
                if load_check == "loaded":
                    answer = askquestion(
                        "Warning!",
                        "Chronological DAG already loaded, do you want to save this as a new model first? \n Click YES to save as new model and NO to overwrite existing model",
                    )
                self.comb_nodes = np.append(self.comb_nodes, self.node)
                graph_temp = nx.contracted_nodes(self.graph, self.comb_nodes[0], self.comb_nodes[1])
                x_nod = list(graph_temp)
                newnode = str(self.comb_nodes[0]) + " = " + str(self.comb_nodes[1])
                y_nod = [newnode if i == self.comb_nodes[0] else i for i in x_nod]
                mapping = dict(zip(x_nod, y_nod))
                graph_temp = nx.relabel_nodes(graph_temp, mapping)
                try:
                    self.graph_check = nx.transitive_reduction(graph_temp)
                    self.graph = graph_temp
                except Exception as e:
                    if e.__class__.__name__ == "NetworkXError":
                        tk.messagebox.showinfo("Error!", "This creates a cycle so you cannot equate these contexts")
                self.OptionList.remove("Equate context with " + str(self.comb_nodes[0]))
                self.testmenu = ttk.OptionMenu(
                    self.littlecanvas, self.variable, self.OptionList[0], *self.OptionList, command=self.nodes
                )
                self.comb_nodes = []
        # sets up menu to equate context for when user picks next node
        if self.variable.get() == "Equate context with another":
            if len(self.comb_nodes) == 1:
                self.OptionList.remove("Equate context with " + str(self.comb_nodes[0]))
                self.testmenu = ttk.OptionMenu(
                    self.littlecanvas, self.variable, self.OptionList[0], *self.OptionList, command=self.nodes
                )
                self.comb_nodes = []
            self.comb_nodes = np.append(self.comb_nodes, self.node)
            self.OptionList.append("Equate context with " + str(self.comb_nodes[0]))
            self.testmenu = ttk.OptionMenu(
                self.littlecanvas, self.variable, self.OptionList[0], *self.OptionList, command=self.nodes
            )

        if self.variable.get() == "Supplementary menu":
            self.w = popupWindow2(self, self.graph, self.canvas)
        if self.variable.get() == "Get supplementary data for this context":
            self.stratinfo = self.stratfunc(self.node)
            self.metadict2 = {}
            self.metadict = self.graph.nodes()[str(self.node)]
            self.metadict2["Contexts above"] = [self.stratinfo[0]]
            self.metadict2["Contexts below"] = [self.stratinfo[1]]
            self.meta1 = pd.DataFrame.from_dict(self.metadict, orient="index")
            self.meta2 = pd.DataFrame.from_dict(self.metadict2, orient="index")
            self.meta = pd.concat([self.meta1, self.meta2])
            self.meta = self.meta.loc["Determination":"Contexts below"]
            self.meta.columns = ["Data"]
            if self.meta.loc["Determination"][0] != "None":
                self.meta.loc["Determination"][0] = (
                    str(self.meta.loc["Determination"][0][0])
                    + " +- "
                    + str(self.meta.loc["Determination"][0][1])
                    + " Carbon BP"
                )
            self.canvas.itemconfig(
                self.metatext_id, text="Supplementary of node " + str(self.node), font="helvetica 12 bold"
            )
            cols = list(self.meta.columns)
            #     self.tree1 = ttk.Treeview(self.canvas)
            clear_all(self.tree1)
            self.tree1["columns"] = cols
            self.tree1.place(relx=0.758, rely=0.725, relwidth=0.225)
            self.tree1.column("Data", anchor="w")
            self.tree1.heading("Data", text="Data", anchor="w")
            for index, row in self.meta.iterrows():
                self.tree1.insert("", 0, text=index, values=list(row))
            self.tree1.update()
        # sets up menu to add strat relationships for when user picks next node
        if self.variable.get() == "Place above other context":
            if len(self.edge_nodes) == 1:
                self.OptionList.remove("Place " + str(self.edge_nodes[0]) + " Above")
                self.testmenu = ttk.OptionMenu(
                    self.littlecanvas, self.variable, self.OptionList[0], *self.OptionList, command=self.nodes
                )
                self.edge_nodes = []
            self.edge_nodes = np.append(self.edge_nodes, self.node)
            self.OptionList.append("Place " + str(self.edge_nodes[0]) + " Above")
            self.testmenu = ttk.OptionMenu(
                self.littlecanvas, self.variable, self.OptionList[0], *self.OptionList, command=self.nodes
            )
        if self.variable.get() == "Get stratigraphic information":
            self.stratfunc(self.node)
        if phase_true == 1:
            imgrender_phase(self.graph)
        else:
            imgrender(self.graph, self.littlecanvas.winfo_width(), self.littlecanvas.winfo_height())
        self.image = Image.open("testdag.png")
        self.width, self.height = self.image.size
        self.container = self.littlecanvas.create_rectangle(0, 0, self.width, self.height, width=0)
        self.show_image()
        self.variable.set("Node Action")
        self.littlecanvas.unbind("<Button-1>")
        self.littlecanvas.bind("<Button-1>", self.move_from)
        self.littlecanvas.bind("<MouseWheel>", self.wheel)

    def move_from(self, event):
        """Remembers previous coordinates for scrolling with the mouse"""
        if self.image != "noimage":
            self.littlecanvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        """Drag (move) canvas to the new position"""
        if self.image != "noimage":
            self.littlecanvas.scan_dragto(event.x, event.y, gain=1)
            self.show_image()

        # redraw the image

    def move_from2(self, event):
        """Remembers previous coordinates for scrolling with the mouse"""
        if self.image2 != "noimage":
            self.littlecanvas2.scan_mark(event.x, event.y)

    def move_to2(self, event):
        """Drag (move) canvas to the new position"""
        if self.image2 != "noimage":
            self.littlecanvas2.scan_dragto(event.x, event.y, gain=1)
            self.show_image()

    def wheel(self, event):
        """Zoom with mouse wheel"""
        x_zoom = self.littlecanvas.canvasx(event.x)
        y_zoom = self.littlecanvas.canvasy(event.y)
        bbox = self.littlecanvas.bbox(self.container)  # get image area
        if bbox[0] < x_zoom < bbox[2] and bbox[1] < y_zoom < bbox[3]:
            pass  # Ok! Inside the image
        else:
            return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30:
                return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.littlecanvas.winfo_width(), self.littlecanvas.winfo_height())
            if i < self.imscale:
                return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale *= self.delta
        #    print(scale)
        self.littlecanvas.scale("all", 0, 0, scale, scale)  # rescale all canvas objects
        self.show_image()

    def wheel2(self, event):
        """Zoom with mouse wheel"""
        x_zoom = self.littlecanvas2.canvasx(event.x)
        y_zoom = self.littlecanvas2.canvasy(event.y)
        bbox = self.littlecanvas2.bbox(self.container2)  # get image area
        if bbox[0] < x_zoom < bbox[2] and bbox[1] < y_zoom < bbox[3]:
            pass  # Ok! Inside the image
        else:
            return  # zoom only inside image area
        scale2 = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width2, self.height2)
            if int(i * self.imscale2) < 30:
                return  # image is less than 30 pixels
            self.imscale2 /= self.delta2
            scale2 /= self.delta2
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.littlecanvas2.winfo_width(), self.littlecanvas2.winfo_height())
            if i < self.imscale2:
                return  # 1 pixel is bigger than the visible area
            self.imscale2 *= self.delta2
            scale2 *= self.delta2
        self.littlecanvas2.scale("all", 0, 0, scale2, scale2)  # rescale all canvas objects
        self.show_image2()

    def show_image(self):
        """Show image on the Canvas"""

        bbox1 = [0, 0, int(self.image.size[0] * self.imscale), int(self.image.size[1] * self.imscale)]
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (
            self.littlecanvas.canvasx(0),  # get visible area of the canvas
            self.littlecanvas.canvasy(0),
            self.littlecanvas.canvasx(self.littlecanvas.winfo_width()),
            self.littlecanvas.canvasy(self.littlecanvas.winfo_height()),
        )
        if int(bbox2[3]) == 1:
            bbox2 = [0, 0, 0.96 * 0.99 * 0.97 * 1000, 0.99 * 0.37 * 2000 * 0.96]
        bbox = [
            min(bbox1[0], bbox2[0]),
            min(bbox1[1], bbox2[1]),  # get scroll region box
            max(bbox1[2], bbox2[2]),
            max(bbox1[3], bbox2[3]),
        ]
        bbox1 = [0, 0, int(self.image.size[0] * self.imscale), int(self.image.size[1] * self.imscale)]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.littlecanvas.configure(scrollregion=bbox)  # set scroll region
        x_1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y_1 = max(bbox2[1] - bbox1[1], 0)
        x_2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y_2 = min(bbox2[3], bbox1[3]) - bbox1[1]

        if int(x_2 - x_1) > 0 and int(y_2 - y_1) > 0:  # show image if it in the visible area
            x_img = min(int(x_2 / self.imscale), self.width)  # sometimes it is larger on 1 pixel
            y_img = min(int(y_2 / self.imscale), self.height)  # ...and sometimes not
            image = self.image.crop((int(x_1 / self.imscale), int(y_1 / self.imscale), x_img, y_img))
            self.imagetk = ImageTk.PhotoImage(image.resize((int(x_2 - x_1), int(y_2 - y_1))))
            self.littlecanvas.delete(self.littlecanvas_img)
            self.imageid = self.littlecanvas.create_image(
                max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]), anchor="nw", image=self.imagetk
            )
            self.transx, self.transy = bbox2[0], bbox2[1]
            self.littlecanvas.imagetk = self.imagetk

    def show_image2(self):
        """Show image on the Canvas"""
        bbox1 = [0, 0, int(self.image2.size[0] * self.imscale2), int(self.image2.size[1] * self.imscale2)]
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (
            self.littlecanvas2.canvasx(0),  # get visible area of the canvas
            self.littlecanvas2.canvasy(0),
            self.littlecanvas2.canvasx(self.littlecanvas2.winfo_width()),
            self.littlecanvas2.canvasy(self.littlecanvas2.winfo_height()),
        )
        if int(bbox2[3]) == 1:
            bbox2 = [0, 0, 0.96 * 0.99 * 0.97 * 1000, 0.99 * 0.37 * 2000 * 0.96]
        bbox = [
            min(bbox1[0], bbox2[0]),
            min(bbox1[1], bbox2[1]),  # get scroll region box
            max(bbox1[2], bbox2[2]),
            max(bbox1[3], bbox2[3]),
        ]
        bbox1 = [0, 0, int(self.image2.size[0] * self.imscale2), int(self.image2.size[1] * self.imscale2)]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.littlecanvas2.configure(scrollregion=bbox)  # set scroll region
        x_1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y_1 = max(bbox2[1] - bbox1[1], 0)
        x_2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y_2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        if int(x_2 - x_1) > 0 and int(y_2 - y_1) > 0:  # show image if it in the visible area
            x_img = min(int(x_2 / self.imscale2), self.width2)  # sometimes it is larger on 1 pixel
            y_img = min(int(y_2 / self.imscale2), self.height2)  # ...and sometimes not
            image2 = self.image2.crop((int(x_1 / self.imscale2), int(y_1 / self.imscale2), x_img, y_img))
            self.imagetk2 = ImageTk.PhotoImage(image2.resize((int(x_2 - x_1), int(y_2 - y_1))))
            self.littlecanvas2.delete(self.littlecanvas2_img)
            self.imageid2 = self.littlecanvas2.create_image(
                max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]), anchor="nw", image=self.imagetk2
            )
            self.transx2, self.transy2 = bbox2[0], bbox2[1]
            self.littlecanvas2.imagetk2 = self.imagetk2

    def phasing(self):
        """runs image render function with phases on seperate levels"""
        global phase_true, node_df
        phase_true = 1
        self.image = imgrender_phase(self.graph)
        self.littlecanvas.img = ImageTk.PhotoImage(self.image)
        self.littlecanvas_img = self.littlecanvas.create_image(0, 0, anchor="nw", image=self.littlecanvas.img)
        self.width, self.height = self.image.size
        #  self.imscale = 1.0  # scale for the canvaas image
        self.delta = 1.1  # zoom magnitude
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.littlecanvas.create_rectangle(0, 0, self.width, self.height, width=0)
        self.imscale = min(921 / self.image.size[0], 702 / self.image.size[1])
        self.littlecanvas.scale("all", 0, 0, self.delta, self.delta)  # rescale all canvas objects
        self.show_image()
        self.bind("<Configure>", self.resize)
        self.littlecanvas.bind("<Configure>", self.resize)
        self.delnodes = []
        self.delnodes_meta = []
        self.canvas.delete("all")
        self.littlecanvas.bind("<Button-3>", self.preClick)
        self.show_image()

    def resize(self, event):
        """resizes image on canvas"""
        img = Image.open("testdag.png")  # .resize((event.width, event.height), Image.ANTIALIAS)
        self.littlecanvas.img = ImageTk.PhotoImage(img)
        self.w_1 = event.width
        self.h_1 = event.height
        self.littlecanvas.itemconfig(self.littlecanvas_img, image=self.littlecanvas.img)

    def resize2(self, event):
        """resizes image on canvas"""
        img = Image.open("testdag_chrono.png")  # .resize((event.width, event.height), Image.ANTIALIAS)
        self.littlecanvas2.img = ImageTk.PhotoImage(img)
        self.w_1 = event.width
        self.h_1 = event.height
        self.littlecanvas2.itemconfig(self.littlecanvas2_img, image=self.littlecanvas2.img)

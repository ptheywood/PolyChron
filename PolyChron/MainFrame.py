
import os
import tkinter as tk
from .globals import POLYCHRON_PROJECTS_DIR
from .load_Window import load_Window

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
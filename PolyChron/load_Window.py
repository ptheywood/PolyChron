
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from .globals import POLYCHRON_PROJECTS_DIR, proj_dir, SCRIPT_DIR
from .PageOne import PageOne

class load_Window(object):
    def __init__(self, master):
        root_x = master.winfo_rootx()
        root_y = master.winfo_rooty()
        self.master = master
        # add offset
        win_x = root_x + 500
        win_y = root_y + 200
        self.top = tk.Toplevel(master)
        self.top.attributes("-topmost", True)
        self.top.title("PolyChron loading page")
        # set toplevel in new position
        self.top.geometry(f"1000x400+{win_x}+{win_y}")
        self.folderPath = tk.StringVar()
        self.maincanvas = tk.Canvas(self.top, bg="white")
        self.maincanvas.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.canvas = tk.Canvas(self.top, bg="#AEC7D6")
        self.canvas.place(relx=0, rely=0, relheight=1, relwidth=0.2)
        self.greeting = None
        self.b = None
        self.c = None
        self.back = None
        self.back1 = None
        self.l = None
        self.selected_langs = None
        self.MyListBox = None
        self.text_1 = None
        self.user_input = None
        self.folder = None
        self.initscreen()

    def initscreen(self):
        [
            x.destroy()
            for x in [
                self.greeting,
                self.b,
                self.c,
                self.back,
                self.back1,
                self.l,
                self.MyListBox,
                self.text_1,
                self.user_input,
            ]
            if x is not None
        ]
        self.maincanvas.update()
        image1 = Image.open(SCRIPT_DIR / "logo.png")
        logo = ImageTk.PhotoImage(image1.resize((360, 70)))
        #       self.imagetk2 = ImageTk.PhotoImage(image2.resize((int(x_2 - x_1), int(y_2 - y_1))))
        self.label1 = tk.Label(self.maincanvas, image=logo, bg="white")
        self.label1.image = logo
        # Position image
        self.label1.place(relx=0.2, rely=0.2, relheight=0.2, relwidth=0.4)
        self.greeting = tk.Label(
            self.maincanvas,
            text="Welcome to PolyChron, how would you like to proceed?",
            bg="white",
            font=("helvetica 12 bold"),
            fg="#2F4858",
            anchor="w",
        )
        self.greeting.place(relx=0.22, rely=0.45)
        self.b = tk.Button(
            self.maincanvas,
            text="Load existing project",
            command=lambda: self.load_proj(),
            bg="#2F4858",
            font=("Helvetica 12 bold"),
            fg="#eff3f6",
        )
        self.b.place(relx=0.8, rely=0.9)
        self.c = tk.Button(
            self.maincanvas,
            text="Create new project",
            command=lambda: self.new_proj(),
            bg="#eff3f6",
            font=("Helvetica 12 bold"),
            fg="#2F4858",
        )
        self.c.place(relx=0.62, rely=0.9)

    # def getFolderPath(self):
    #     self.top.attributes("-topmost", False)
    #     folder_selected = tk.filedialog.askdirectory()
    #     self.folderPath.set(folder_selected)
    #     os.chdir(self.folderPath.get())

    def load_proj(self):
        global proj_dir
        os.chdir(POLYCHRON_PROJECTS_DIR)
        [
            x.destroy()
            for x in [
                self.label1,
                self.greeting,
                self.b,
                self.c,
                self.back,
                self.l,
                self.back1,
                self.MyListBox,
                self.text_1,
                self.user_input,
            ]
            if x is not None
        ]
        self.maincanvas.update()

        self.l = tk.Label(self.maincanvas, text="Select project", bg="white", font=("helvetica 14 bold"), fg="#2F4858")
        self.l.place(relx=0.36, rely=0.1)
        myList = [d for d in os.listdir(POLYCHRON_PROJECTS_DIR) if os.path.isdir(d)]
        myList = [d for d in myList if (d != "__pycache__") and (d != "Data")]
        mylist_var = tk.StringVar(value=myList)
        self.MyListBox = tk.Listbox(
            self.maincanvas,
            listvariable=mylist_var,
            bg="#eff3f6",
            font=("Helvetica 11 bold"),
            fg="#2F4858",
            selectmode="browse",
        )
        scrollbar = ttk.Scrollbar(self.maincanvas, orient="vertical", command=self.MyListBox.yview)
        self.MyListBox["yscrollcommand"] = scrollbar.set
        self.MyListBox.place(relx=0.36, rely=0.17, relheight=0.4, relwidth=0.28)
        self.MyListBox.bind("<<ListboxSelect>>", self.items_selected)
        self.b = tk.Button(
            self.maincanvas,
            text="Load project",
            command=lambda: self.load_model(proj_dir),
            bg="#2F4858",
            font=("Helvetica 12 bold"),
            fg="#eff3f6",
        )
        self.b.place(relx=0.8, rely=0.9, relwidth=0.19)
        self.top.bind("<Return>", (lambda event: self.load_model(proj_dir)))
        self.back = tk.Button(
            self.maincanvas,
            text="Back",
            command=lambda: self.initscreen(),
            bg="#eff3f6",
            font=("Helvetica 12 bold"),
            fg="#2F4858",
        )
        self.back.place(relx=0.21, rely=0.01)

    def load_model(self, direc):
        global proj_dir
        [
            x.destroy()
            for x in [self.greeting, self.label1, self.b, self.c, self.back, self.back1, self.l, self.MyListBox]
            if x is not None
        ]
        if self.selected_langs is None:
            path = direc
        else:
            path = os.getcwd() + "/" + self.selected_langs
        os.chdir(path)
        self.maincanvas.update()

        self.l = tk.Label(self.maincanvas, text="Model list", bg="white", font=("helvetica 14 bold"), fg="#2F4858")
        self.l.place(relx=0.36, rely=0.1)
        # myList_all = os.listdir(POLYCHRON_PROJECTS_DIR)
        myList = [d for d in os.listdir(path) if os.path.isdir(d)]
        self.model_list = tk.StringVar(value=myList)
        self.MyListBox = tk.Listbox(
            self.maincanvas,
            listvariable=self.model_list,
            bg="#eff3f6",
            font=("Helvetica 11 bold"),
            fg="#2F4858",
            selectmode="browse",
        )
        scrollbar = ttk.Scrollbar(self.maincanvas, orient="vertical", command=self.MyListBox.yview)
        self.MyListBox["yscrollcommand"] = scrollbar.set
        self.MyListBox.place(relx=0.36, rely=0.17, relheight=0.4, relwidth=0.28)
        self.MyListBox.bind("<<ListboxSelect>>", self.items_selected)
        self.b = tk.Button(
            self.maincanvas,
            text="Load selected model",
            command=lambda: self.cleanup2(),
            bg="#2F4858",
            font=("Helvetica 12 bold"),
            fg="#eff3f6",
        )
        self.top.bind("<Return>", (lambda event: self.cleanup2()))
        self.b.place(relx=0.8, rely=0.9, relwidth=0.195)
        self.back = tk.Button(
            self.maincanvas,
            text="Back",
            command=lambda: self.initscreen(),
            bg="#eff3f6",
            font=("Helvetica 12 bold"),
            fg="#2F4858",
        )
        self.back.place(relx=0.21, rely=0.01)
        self.back1 = tk.Button(
            self.maincanvas,
            text="Create new model",
            command=lambda: self.new_model(path),
            bg="#eff3f6",
            font=("Helvetica 12 bold"),
            fg="#2F4858",
        )
        self.back1.place(relx=0.62, rely=0.9, relwidth=0.17)
        proj_dir = path

    def items_selected(self, event):
        """handle item selected event"""
        # get selected indices
        selected_indices = self.MyListBox.curselection()
        # get selected items
        self.selected_langs = ",".join([self.MyListBox.get(i) for i in selected_indices])

    def create_file(self, folder_dir, load):
        from .StartPage import StartPage

        global proj_dir
        dirs = os.path.join(POLYCHRON_PROJECTS_DIR, folder_dir, self.model.get())
        dirs2 = os.path.join(dirs, "stratigraphic_graph")
        dirs3 = os.path.join(dirs, "chronological_graph")
        dirs4 = os.path.join(dirs, "python_only")
        dirs5 = os.path.join(dirs, "mcmc_results")
        if not os.path.exists(dirs):
            #     os.makedirs(dirs)
            os.makedirs(dirs)
            os.makedirs(dirs2)
            os.makedirs(dirs3)
            os.makedirs(dirs4)
            os.makedirs(dirs5)
            os.chdir(dirs)
            proj_dir = os.path.join(POLYCHRON_PROJECTS_DIR, folder_dir)
            if load:
                for F in (StartPage, PageOne):
                    page_name = F.__name__
                    frame = F(parent=self.master.container, controller=self.master)
                    self.master.frames[page_name] = frame

                    # put all of the pages in the same location;
                    # the one on the top of the stacking order
                    # will be the one that is visible.
                    frame.grid(row=0, column=0, sticky="nsew")
                    self.master.show_frame("StartPage")
            self.cleanup()
            tk.messagebox.showinfo("Tips:", "model created successfully!")
            os.chdir(dirs)
        else:
            tk.messagebox.showerror("Tips", "The folder name exists, please change it")
            self.cleanup()

    def new_proj(self):
        [
            x.destroy()
            for x in [
                self.greeting,
                self.label1,
                self.b,
                self.back1,
                self.c,
                self.back,
                self.l,
                self.MyListBox,
                self.text_1,
                self.user_input,
            ]
            if x is not None
        ]
        self.maincanvas.update()
        self.folder = tk.StringVar()  # Receiving user's folder_name selection
        self.text_1 = tk.Label(
            self.maincanvas, text="Input project name:", bg="white", font=("helvetica 14 bold"), fg="#2F4858"
        )
        self.text_1.place(relx=0.4, rely=0.2)
        self.user_input = tk.Entry(self.maincanvas, textvariable=self.folder)
        self.user_input.place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.08)
        self.b = tk.Button(
            self.maincanvas,
            text="Submit ",
            command=lambda: self.new_model(self.folder.get()),
            bg="#ec9949",
            font=("Helvetica 12 bold"),
            fg="#2F4858",
        )
        self.top.bind("<Return>", (lambda event: self.new_model(self.folder.get())))
        self.b.place(relx=0.66, rely=0.4)
        self.back = tk.Button(
            self.maincanvas,
            text="Back",
            command=lambda: self.initscreen(),
            bg="#dcdcdc",
            font=("helvetica 12 bold"),
            fg="#2F4858",
        )
        self.back.place(relx=0.21, rely=0.01)

    def new_model(self, folder_dir, load=True):
        [
            x.destroy()
            for x in [
                self.greeting,
                self.label1,
                self.b,
                self.c,
                self.back,
                self.back1,
                self.l,
                self.MyListBox,
                self.text_1,
                self.user_input,
            ]
            if x is not None
        ]
        self.maincanvas.update()
        self.model = tk.StringVar()  # Receiving user's folder_name selection
        self.text_1 = tk.Label(
            self.maincanvas, text="Input model name:", bg="white", font=("helvetica 14 bold"), fg="#2F4858"
        )
        self.text_1.place(relx=0.4, rely=0.2)
        self.user_input = tk.Entry(self.maincanvas, textvariable=self.model)
        self.user_input.place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.08)
        self.b = tk.Button(
            self.maincanvas,
            text="Submit ",
            command=lambda: self.create_file(folder_dir, load),
            bg="#ec9949",
            font=("Helvetica 12 bold"),
            fg="#2F4858",
        )
        self.b.place(relx=0.66, rely=0.4)
        self.top.bind("<Return>", (lambda event: self.create_file(folder_dir, load)))
        self.back = tk.Button(
            self.maincanvas,
            text="Back",
            command=lambda: self.new_proj(),
            bg="#dcdcdc",
            font=("helvetica 12 bold"),
            fg="#2F4858",
        )
        self.back.place(relx=0.21, rely=0.01)
        return self.top

    def cleanup(self):
        self.top.destroy()

    def cleanup2(self):
        from .StartPage import StartPage


        path = os.getcwd() + "/" + self.selected_langs
        os.chdir(path)
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=self.master.container, controller=self.master)
            self.master.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.master.show_frame("StartPage")
        self.top.destroy()

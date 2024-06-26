import os
import ctypes
import platform
import tkinter as tk
from tkinter import ttk
from app.pages.ssh import SSHPage
from app.pages.install import InstallPage
from app.pages.home import HomePage
from app.pages.monitoring import MonitoringPage
from app.pages.settings import SettingsPage


def is_windows():
    return platform.system() == "Windows"

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.controller = PageController(self)
        self.title("EasyPot")
        myappid = 'SEGRED.EasyPot.artillery.1'
        if is_windows():
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setup_icon()
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.pages = {}
        self.notebook = None
        
        self.setup_pages()
    
    def setup_icon(self):
        try:
            current_directory = os.getcwd()
            icon_path = os.path.join(current_directory, "app", "static", "images", "honey.png")
            icon = tk.PhotoImage(file=icon_path)
            self.wm_iconphoto(True, icon)
            if is_windows():
                icon_path = os.path.join(current_directory, "app", "static", "images", "honey.ico")
                self.iconbitmap(icon_path)
        except Exception as e:
            print("Failed to set icon: ", e)

    def setup_pages(self):
        for Page in (SSHPage, InstallPage):
            page_name = Page.__name__
            frame = Page(parent=self.container, controller=self.controller)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.controller.show_page("SSHPage")

    def start_notebook(self):
        self.notebook = ttk.Notebook(self.container)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        for Page in (HomePage, MonitoringPage, SettingsPage):
            page_name = Page.__name__
            frame = Page(parent=self.notebook, controller=self.controller)
            self.pages[page_name] = frame
            self.notebook.add(frame, text=page_name)

    def run(self):
        self.mainloop()


class PageController:
    def __init__(self, app):
        self.app = app

    def show_page(self, page_name):
        if page_name in self.app.pages:
            if page_name in ['SSHPage', 'InstallPage']:
                if self.app.notebook:
                    self.app.notebook.grid_remove()
                page = self.app.pages[page_name]
                page.grid()
                page.tkraise()
                if is_windows():
                    self.set_page_size(380, 160)
                else:
                    self.set_page_size(480, 160)
                self.app.eval('tk::PlaceWindow . center')
            else:
                self.app.pages['SSHPage'].grid_remove()
                self.app.pages['InstallPage'].grid_remove()
                self.app.notebook.grid()
                self.app.notebook.select(self.app.pages[page_name])
                if is_windows():
                    self.set_page_size(630, 430)
                else:
                    self.set_page_size(750, 430)
                self.app.eval('tk::PlaceWindow . center')
            
        else:
            print(f"Page '{page_name}' not found in app.pages")

    def set_page_size(self, width, height):
        self.app.geometry(f"{width}x{height}")

    def open_notebook(self):
        self.app.start_notebook()
    
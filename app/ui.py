import os
import ctypes
import tkinter as tk
from tkinter import ttk
from app.pages.ssh import SSHPage
from app.pages.install import InstallPage
from app.pages.home import HomePage
from app.pages.monitoring import MonitoringPage
from app.pages.settings import SettingsPage


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.controller = PageController(self)
        self.title("EasyPot")
        myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setup_icon()
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.pages = {}
        
        self.setup_pages()
    
    def setup_icon(self):
        try:
            current_directory = os.getcwd()
            small_icon_path = os.path.join(current_directory, "app", "static", "images", "honey16.png")
            large_icon_path = os.path.join(current_directory, "app", "static", "images", "honey32.png")
            small_icon = tk.PhotoImage(file=small_icon_path)
            large_icon = tk.PhotoImage(file=large_icon_path)
            self.wm_iconphoto(True, large_icon, small_icon)
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

        self.notebook = ttk.Notebook(self.container)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        for Page in (HomePage, MonitoringPage, SettingsPage):
            page_name = Page.__name__
            frame = Page(parent=self.notebook, controller=self.controller)
            self.pages[page_name] = frame
            self.notebook.add(frame, text=page_name.replace("Page", ""))

        self.controller.show_page("SSHPage")

    def run(self):
        self.mainloop()

class PageController:
    def __init__(self, app):
        self.app = app

    def show_page(self, page_name):
        if page_name in self.app.pages:
            if page_name in ['SSHPage', 'InstallPage']:
                self.app.notebook.grid_remove()
                page = self.app.pages[page_name]
                page.grid()
                page.tkraise()
                self.set_page_size(380, 160) 
                self.app.eval('tk::PlaceWindow . center')
            else:
                self.app.pages['SSHPage'].grid_remove()
                self.app.pages['InstallPage'].grid_remove()
                self.app.notebook.grid()
                self.app.notebook.select(self.app.pages[page_name])
                self.set_page_size(570, 400)
                self.app.eval('tk::PlaceWindow . center')
            if hasattr(self.app.pages[page_name], 'on_show'):
                self.app.pages[page_name].on_show()

    def set_page_size(self, width, height):
        self.app.geometry(f"{width}x{height}")


if __name__ == "__main__":
    app = App()
    app.run()

import tkinter as tk
from tkinter import messagebox
from app.controllers.ssh_controller import SSHController

class SSHPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.mainController = controller
        self.pageController = SSHController()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="SSH Connection", font=("Helvetica", 16))
        self.title_label.grid(row=0, columnspan=4, pady=10)

        self.hostname_label = tk.Label(self, text="Hostname:")
        self.hostname_label.grid(row=1, column=0, pady=5)
        self.hostname_entry = tk.Entry(self)
        self.hostname_entry.insert(tk.END, "faria-afonso.pt")
        self.hostname_entry.grid(row=1, column=1, pady=5)

        self.port_label = tk.Label(self, text="Port:")
        self.port_label.grid(row=1, column=2, pady=0)
        self.port_entry = tk.Entry(self)
        self.port_entry.insert(tk.END, "22") 
        self.port_entry.grid(row=1, column=3, pady=5)

        self.username_label = tk.Label(self, text="Username:")
        self.username_label.grid(row=2, column=0, pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.insert(tk.END, "root")
        self.username_entry.grid(row=2, column=1, pady=5)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=2, column=2, pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.insert(tk.END, "4Ur94J9GtZj1oBv")
        self.password_entry.grid(row=2, column=3, pady=5)

        self.connect_button = tk.Button(self, text="Connect", command=self.connect_ssh)
        self.connect_button.grid(row=4, columnspan=4, pady=10)

    def connect_ssh(self):
        hostname = self.hostname_entry.get()
        port = int(self.port_entry.get())
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not all([hostname, port, username, password]):
            messagebox.showerror("Error", "All fields are required")
            return

        result = self.pageController.connect(hostname, port, username, password)
        if result == "Connected successfully":
            if self.pageController.is_root(): 
                messagebox.showinfo("Connection Status", result)
                _installed = self.pageController.check_installed()
                if _installed:
                    self.mainController.open_notebook()
                    self.mainController.show_page("HomePage")
                else:
                    self.mainController.show_page("InstallPage")
            else:
                self.pageController.disconnect()
                messagebox.showerror("Error", "You must be root to connect")
        else: 
            self.pageController.disconnect()
            messagebox.showerror("Connection Error", result)

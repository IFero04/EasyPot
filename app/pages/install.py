import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.install_controller import InstallController


class InstallPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.mainController = controller
        self.pageController = InstallController()

        self.create_widgets()

        self.update_progress(0)

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Install Artillery", font=("Helvetica", 16))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.progress_label = tk.Label(self, text="Progress:")
        self.progress_label.grid(row=1, column=0, pady=5)

        self.progressbar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progressbar.grid(row=1, column=1, pady=5)

        self.install_button = tk.Button(self, text="Confirm", command=self.install)
        self.install_button.grid(row=2, column=0, pady=10, padx=5)

        self.cancel_button = tk.Button(self, text="Cancel", command=self.cancel)
        self.cancel_button.grid(row=2, column=1, pady=10, padx=5)

        # Configure grid to center widgets
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def update_progress(self, value):
        self.progressbar["value"] = value
        self.update_idletasks()

    def install(self):
        try:
            self.pageController.send_file()
            self.update_progress(30) 
            self.pageController.unzip_and_run_setup(self.update_progress)
            self.update_progress(90)
            if self.pageController.check_installed(self.update_progress):
                self.update_progress(100)
                messagebox.showinfo("Success", "Artillery installed successfully")
                self.mainController.show_page("HomePage")
                self.update_progress(0)
            
            
        except Exception as e:
            print(e)
            messagebox.showerror("Error", str(e))

    def cancel(self):
        self.pageController.disconnect()
        self.mainController.show_page("SSHPage")

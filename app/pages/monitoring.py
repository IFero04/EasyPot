import tkinter as tk
from tkinter import scrolledtext, filedialog
from app.controllers.monitoring_controller import MonitoringController

class MonitoringPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.mainController = controller
        self.pageController = MonitoringController()

        self.create_widgets()
        self.is_monitoring = False
        self.start_monitoring()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(self, text="Monitoring Page", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.setup_label = tk.Label(self, text="Setup Log - Unknown", font=("Helvetica", 12))
        self.setup_label.grid(row=1, column=0, padx=20, pady=5)

        self.setup_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=15, width=50, state=tk.DISABLED)
        self.setup_text.grid(row=2, column=0, padx=20, pady=5)

        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=3, column=0, pady=10)

        start_button = tk.Button(buttons_frame, text="Start Monitoring", command=self.start_monitoring)
        start_button.grid(row=0, column=0, padx=5)

        download_button = tk.Button(buttons_frame, text="Download Logs", command=self.download_logs)
        download_button.grid(row=0, column=1, padx=5)

        stop_button = tk.Button(buttons_frame, text="Stop Monitoring", command=self.stop_monitoring)
        stop_button.grid(row=0, column=2, padx=5)

    def start_monitoring(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.pageController.start_reading(self.setup_text)
            self.setup_label.config(text="Setup Log - Active")

    def stop_monitoring(self):
        if self.is_monitoring:
            self.is_monitoring = False
            self.pageController.stop_reading()
            self.setup_label.config(text="Setup Log - Stopped")

    def download_logs(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.pageController.download_log(file_path)

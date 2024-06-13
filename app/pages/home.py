import tkinter as tk
from tkinter import messagebox
from app.controllers.home_controller import HomeController

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.mainController = controller
        self.pageController = HomeController()

        self.create_widgets()
        self.refresh_page()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title_label = tk.Label(self, text="Server Management", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Left side: Server controls
        self.server_status_label = tk.Label(self, text="Server Status: Unknown", font=("Helvetica", 12))
        self.server_status_label.grid(row=1, column=0, padx=20, pady=5)

        self.stop_start_button = tk.Button(self, text="Start Server", command=self.stop_start_server)
        self.stop_start_button.grid(row=2, column=0, pady=5, padx=20)

        self.restart_button = tk.Button(self, text="Restart Server", command=self.restart_server)
        self.restart_button.grid(row=3, column=0, pady=5, padx=20)

        self.uninstall_button = tk.Button(self, text="Uninstall Server", command=self.uninstall_server)
        self.uninstall_button.grid(row=4, column=0, pady=5, padx=20)

        self.refresh_button = tk.Button(self, text="Refresh", command=self.refresh_page)
        self.refresh_button.grid(row=5, column=0, pady=5, padx=20)

        self.close_button = tk.Button(self, text="Close Connection", command=self.close_connection)
        self.close_button.grid(row=6, column=0, pady=10, padx=20)

        # Right side: Banned IPs
        self.banned_ips_label = tk.Label(self, text="Banned IPs", font=("Helvetica", 12))
        self.banned_ips_label.grid(row=1, column=1, padx=20, pady=5)

        self.banned_ips_listbox = tk.Listbox(self, selectmode=tk.SINGLE, width=50)
        self.banned_ips_listbox.grid(row=2, column=1, rowspan=3, pady=5, padx=20)

        self.remove_ban_button = tk.Button(self, text="Remove Selected Ban", command=self.remove_selected_ban)
        self.remove_ban_button.grid(row=5, column=1, pady=5, padx=20)

        self.purge_bans_button = tk.Button(self, text="Purge Bans", command=self.purge_bans)
        self.purge_bans_button.grid(row=6, column=1, pady=(5, 20), padx=20)

    def close_connection(self):
        self.pageController.disconnect()
        self.mainController.show_page("SSHPage")
    
    def update_server_status(self):
        try:
            if self.pageController.check_artillery_status():
                self.server_status_label.config(text="Server Status: Active")
                self.stop_start_button.config(text="Stop Server")
            else:
                self.server_status_label.config(text="Server Status: Inactive")
                self.stop_start_button.config(text="Start Server")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_start_server(self):
        try:
            if self.pageController.check_artillery_status():
                self.pageController.stop_server()
                messagebox.showinfo("Success", "Server stopped successfully")
            else:
                self.pageController.start_server()
                messagebox.showinfo("Success", "Server started successfully")
            self.update_server_status()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def restart_server(self):
        try:
            self.pageController.stop_server()
            self.pageController.start_server()
            messagebox.showinfo("Success", "Server restarted successfully")
            self.update_server_status()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def uninstall_server(self):
        try:
            self.pageController.uninstall_server()
            self.update_server_status()
            messagebox.showinfo("Success", "Server uninstalled successfully")
            self.pageController.disconnect()
            self.mainController.show_page("SSHPage")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_banned_ips(self):
        try:
            self.banned_ips_listbox.delete(0, tk.END)
            banned_ips = self.pageController.get_banned_ips()
            if banned_ips:
                for ip in banned_ips:
                    self.banned_ips_listbox.insert(tk.END, ip)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_selected_ban(self):
        selected_ip = self.banned_ips_listbox.get(tk.ACTIVE)
        if selected_ip:
            try:
                self.pageController.remove_ban(selected_ip)
                self.refresh_banned_ips()
                messagebox.showinfo("Success", f"Ban removed for IP: {selected_ip}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def purge_bans(self):
        try:
            self.pageController.purge_bans()
            self.refresh_banned_ips()
            messagebox.showinfo("Success", "All bans purged successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def refresh_page(self):
        self.update_server_status()
        self.refresh_banned_ips()

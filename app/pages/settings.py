import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.settings_controller import SettingsController


class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.mainController = controller
        self.pageController = SettingsController()

        self.create_widgets()
        self.refresh_settings()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Title
        self.title_label = tk.Label(self, text="Settings", font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=8, pady=10)

        # Monitoring Section
        monitoring_label = tk.Label(self, text="Monitoring", font=("Helvetica", 12))
        monitoring_label.grid(row=1, column=0, columnspan=2, pady=5)

        monitor_label = tk.Label(self, text="Monitor:")
        monitor_label.grid(row=2, column=0, sticky=tk.W, padx=5)
        self.monitor_var = tk.BooleanVar()
        monitor_checkbox = ttk.Checkbutton(self, variable=self.monitor_var)
        monitor_checkbox.grid(row=2, column=1, sticky=tk.W, padx=5)

        monitor_folders_label = tk.Label(self, text="Monitor Folders:")
        monitor_folders_label.grid(row=3, column=0, sticky=tk.W, padx=5)
        self.monitor_folders_var = tk.StringVar()
        monitor_folders_entry = tk.Entry(self, textvariable=self.monitor_folders_var)
        monitor_folders_entry.grid(row=3, column=1, sticky=tk.W, padx=5)

        system_hardening_label = tk.Label(self, text="System Hardening:")
        system_hardening_label.grid(row=4, column=0, sticky=tk.W, padx=5)
        self.system_hardening_var = tk.BooleanVar()
        system_hardening_checkbox = ttk.Checkbutton(self, variable=self.system_hardening_var)
        system_hardening_checkbox.grid(row=4, column=1, sticky=tk.W, padx=5)

        ssh_default_port_label = tk.Label(self, text="SSH Default Port Check:")
        ssh_default_port_label.grid(row=5, column=0, sticky=tk.W, padx=5)
        self.ssh_default_port_var = tk.BooleanVar()
        ssh_default_port_checkbox = ttk.Checkbutton(self, variable=self.ssh_default_port_var)
        ssh_default_port_checkbox.grid(row=5, column=1, sticky=tk.W, padx=5)

        exclude_label = tk.Label(self, text="Exclude:")
        exclude_label.grid(row=6, column=0, sticky=tk.W, padx=5)
        self.exclude_var = tk.StringVar()
        exclude_entry = tk.Entry(self, textvariable=self.exclude_var)
        exclude_entry.grid(row=6, column=1, sticky=tk.W, padx=5)

        # Honeypot Section
        honeypot_label = tk.Label(self, text="Honeypot", font=("Helvetica", 12))
        honeypot_label.grid(row=1, column=2, columnspan=2, pady=5)

        honeypot_ban_label = tk.Label(self, text="Honeypot Ban:")
        honeypot_ban_label.grid(row=2, column=2, sticky=tk.W, padx=5)
        self.honeypot_ban_var = tk.BooleanVar()
        honeypot_ban_checkbox = ttk.Checkbutton(self, variable=self.honeypot_ban_var)
        honeypot_ban_checkbox.grid(row=2, column=3, sticky=tk.W, padx=5)

        whitelist_ip_label = tk.Label(self, text="Whitelist IP:")
        whitelist_ip_label.grid(row=3, column=2, sticky=tk.W, padx=5)
        self.whitelist_ip_var = tk.StringVar()
        whitelist_ip_entry = tk.Entry(self, textvariable=self.whitelist_ip_var)
        whitelist_ip_entry.grid(row=3, column=3, sticky=tk.W, padx=5)

        tcp_ports_label = tk.Label(self, text="TCP Ports:")
        tcp_ports_label.grid(row=4, column=2, sticky=tk.W, padx=5)
        self.tcp_ports_var = tk.StringVar()
        tcp_ports_entry = tk.Entry(self, textvariable=self.tcp_ports_var)
        tcp_ports_entry.grid(row=4, column=3, sticky=tk.W, padx=5)

        udp_ports_label = tk.Label(self, text="UDP Ports:")
        udp_ports_label.grid(row=5, column=2, sticky=tk.W, padx=5)
        self.udp_ports_var = tk.StringVar()
        udp_ports_entry = tk.Entry(self, textvariable=self.udp_ports_var)
        udp_ports_entry.grid(row=5, column=3, sticky=tk.W, padx=5)

        honeypot_autoaccept_label = tk.Label(self, text="Honeypot Auto Accept:")
        honeypot_autoaccept_label.grid(row=6, column=2, sticky=tk.W, padx=5)
        self.honeypot_autoaccept_var = tk.BooleanVar()
        honeypot_autoaccept_checkbox = ttk.Checkbutton(self, variable=self.honeypot_autoaccept_var)
        honeypot_autoaccept_checkbox.grid(row=6, column=3, sticky=tk.W, padx=5)

        # Anti-Bruteforce Section
        anti_bruteforce_label = tk.Label(self, text="Anti-Bruteforce", font=("Helvetica", 12))
        anti_bruteforce_label.grid(row=7, column=0, columnspan=2, pady=5)

        ssh_brute_monitor_label = tk.Label(self, text="SSH Brute Monitor:")
        ssh_brute_monitor_label.grid(row=8, column=0, sticky=tk.W, padx=5)
        self.ssh_brute_monitor_var = tk.BooleanVar()
        ssh_brute_monitor_checkbox = ttk.Checkbutton(self, variable=self.ssh_brute_monitor_var)
        ssh_brute_monitor_checkbox.grid(row=8, column=1, sticky=tk.W, padx=5)

        ssh_brute_attempts_label = tk.Label(self, text="SSH Brute Attempts:")
        ssh_brute_attempts_label.grid(row=9, column=0, sticky=tk.W, padx=5)
        self.ssh_brute_attempts_var = tk.StringVar()
        ssh_brute_attempts_entry = tk.Entry(self, textvariable=self.ssh_brute_attempts_var)
        ssh_brute_attempts_entry.grid(row=9, column=1, sticky=tk.W, padx=5)

        ftp_brute_monitor_label = tk.Label(self, text="FTP Brute Monitor:")
        ftp_brute_monitor_label.grid(row=10, column=0, sticky=tk.W, padx=5)
        self.ftp_brute_monitor_var = tk.BooleanVar()
        ftp_brute_monitor_checkbox = ttk.Checkbutton(self, variable=self.ftp_brute_monitor_var)
        ftp_brute_monitor_checkbox.grid(row=10, column=1, sticky=tk.W, padx=5)

        ftp_brute_attempts_label = tk.Label(self, text="FTP Brute Attempts:")
        ftp_brute_attempts_label.grid(row=11, column=0, sticky=tk.W, padx=5)
        self.ftp_brute_attempts_var = tk.StringVar()
        ftp_brute_attempts_entry = tk.Entry(self, textvariable=self.ftp_brute_attempts_var)
        ftp_brute_attempts_entry.grid(row=11, column=1, sticky=tk.W, padx=5)

        anti_dos_label = tk.Label(self, text="Anti-DoS:")
        anti_dos_label.grid(row=12, column=0, sticky=tk.W, padx=5)
        self.anti_dos_var = tk.BooleanVar()
        anti_dos_checkbox = ttk.Checkbutton(self, variable=self.anti_dos_var)
        anti_dos_checkbox.grid(row=12, column=1, sticky=tk.W, padx=5)

        anti_dos_ports_label = tk.Label(self, text="Anti-DoS Ports:")
        anti_dos_ports_label.grid(row=13, column=0, sticky=tk.W, padx=5)
        self.anti_dos_ports_var = tk.StringVar()
        anti_dos_ports_entry = tk.Entry(self, textvariable=self.anti_dos_ports_var)
        anti_dos_ports_entry.grid(row=13, column=1, sticky=tk.W, padx=5)

        # Buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=7, column=2, columnspan=2, sticky=tk.N, pady=10)

        upload_button = tk.Button(buttons_frame, text="Update Config", command=self.update_settings)
        upload_button.grid(row=0, column=0, pady=5, padx=10)

        download_button = tk.Button(buttons_frame, text="Refresh Config", command=self.refresh_settings)
        download_button.grid(row=0, column=1, pady=5, padx=10)

        refresh_button = tk.Button(buttons_frame, text="Reset Config", command=self.reset_settings)
        refresh_button.grid(row=0, column=2, pady=5, padx=10)
    
    def __get_settings(self):
        settings = {
            'MONITOR': self.monitor_var.get(),
            'MONITOR_FOLDERS': self.monitor_folders_var.get(),
            'SYSTEM_HARDENING': self.system_hardening_var.get(),
            'SSH_DEFAULT_PORT_CHECK': self.ssh_default_port_var.get(),
            'EXCLUDE': self.exclude_var.get(),
            'HONEYPOT_BAN': self.honeypot_ban_var.get(),
            'WHITELIST_IP': self.whitelist_ip_var.get(),
            'TCPPORTS': self.tcp_ports_var.get(),
            'UDPPORTS': self.udp_ports_var.get(),
            'HONEYPOT_AUTOACCEPT': self.honeypot_autoaccept_var.get(),
            'SSH_BRUTE_MONITOR': self.ssh_brute_monitor_var.get(),
            'SSH_BRUTE_ATTEMPTS': self.ssh_brute_attempts_var.get(),
            'FTP_BRUTE_MONITOR': self.ftp_brute_monitor_var.get(),
            'FTP_BRUTE_ATTEMPTS': self.ftp_brute_attempts_var.get(),
            'ANTI_DOS': self.anti_dos_var.get(),
            'ANTI_DOS_PORTS': self.anti_dos_ports_var.get()
        }
        return settings

    def __load_settings(self, settings_dict):
        self.monitor_var.set(settings_dict.get('MONITOR', False))
        self.monitor_folders_var.set(settings_dict.get('MONITOR_FOLDERS', ''))
        self.system_hardening_var.set(settings_dict.get('SYSTEM_HARDENING', False))
        self.ssh_default_port_var.set(settings_dict.get('SSH_DEFAULT_PORT_CHECK', False))
        self.exclude_var.set(settings_dict.get('EXCLUDE', ''))
        self.honeypot_ban_var.set(settings_dict.get('HONEYPOT_BAN', False))
        self.whitelist_ip_var.set(settings_dict.get('WHITELIST_IP', ''))
        self.tcp_ports_var.set(settings_dict.get('TCPPORTS', ''))
        self.udp_ports_var.set(settings_dict.get('UDPPORTS', ''))
        self.honeypot_autoaccept_var.set(settings_dict.get('HONEYPOT_AUTOACCEPT', False))
        self.ssh_brute_monitor_var.set(settings_dict.get('SSH_BRUTE_MONITOR', False))
        self.ssh_brute_attempts_var.set(settings_dict.get('SSH_BRUTE_ATTEMPTS', ''))
        self.ftp_brute_monitor_var.set(settings_dict.get('FTP_BRUTE_MONITOR', False))
        self.ftp_brute_attempts_var.set(settings_dict.get('FTP_BRUTE_ATTEMPTS', ''))
        self.anti_dos_var.set(settings_dict.get('ANTI_DOS', False))
        self.anti_dos_ports_var.set(settings_dict.get('ANTI_DOS_PORTS', ''))

    def refresh_settings(self):
        try:
            settings_dict = self.pageController.get_settings()
            self.__load_settings(settings_dict)
        except Exception as e:
            messagebox.showerror("Error", e)

    def update_settings(self):
        try:
            settings = self.__get_settings()
            self.pageController.update_settings(settings)
            messagebox.showinfo("Success", "Settings updated successfully")
        except Exception as e:
            messagebox.showerror("Error", e)

    def reset_settings(self):
        try:
            self.pageController.reset_settings()
            self.refresh_settings()
            
            messagebox.showinfo("Success", "Settings reset successfully")
        except Exception as e:
            messagebox.showerror("Error", e)
        



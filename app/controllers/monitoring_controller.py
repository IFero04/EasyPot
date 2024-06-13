import threading
import tkinter as tk
from app.services.ssh_service import SSHClientSingleton

class MonitoringController:
    def __init__(self):
        self.client = SSHClientSingleton()

    def __execute_command(self, command):
        client = self.client.get_client()
        _, stdout, stderr = client.exec_command(command, get_pty=True)
        return stdout, stderr
        
    def start_monitoring(self):
        print("Started Monitoring")
        
        command = "tail -f /var/artillery/logs/alerts.log"
        stdout, _ = self.__execute_command(command)

        return stdout

    def update_text_widget(self, stdout, text_widget):
        for line in iter(stdout.readline, ""):
            if line:
                text_widget.configure(state=tk.NORMAL)
                text_widget.insert(tk.END, line)
                text_widget.see(tk.END)
                text_widget.configure(state=tk.DISABLED)

    def start_reading(self, text_widget):
        stdout = self.start_monitoring()
        threading.Thread(target=self.update_text_widget, args=(stdout, text_widget), daemon=True).start()

    def stop_reading(self):
        command = "killall tail"
        self.__execute_command(command)
    
    def download_log(self, file_path):
        sftp = self.client.get_client().open_sftp()
        remote_path = "/var/artillery/logs/alerts.log"
        sftp.get(remote_path, file_path)
        sftp.close()
     
        

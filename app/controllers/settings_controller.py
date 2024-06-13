from app.services.ssh_service import SSHClientSingleton
from app.models.settings_model import settings_keys, settings_defaults

class SettingsController:
    def __init__(self):
        self.client = SSHClientSingleton()

    def __execute_command(self, command):
        client = self.client.get_client()
        _, stdout, stderr = client.exec_command(command, get_pty=True)
        return stdout, stderr
    
    def check_artillery_status(self):
        command = "ps -A x | grep artiller[y]"
        stdout, _ = self.__execute_command(command)
        if stdout:
            if "/var/artillery/artillery.py" in stdout.read().decode():
                return True
        return False

    def __stop_server(self):
        commands = [
            "python3 /var/artillery/kill.py",
            "screen -wipe artillery_run"
        ]
        for command in commands:
            _, stderr = self.__execute_command(command)
            if stderr.read().decode():
                raise Exception(stderr.read().decode())

    def get_settings(self):
        settings = {}
        command = "cat /var/artillery/config"
        stdout, _ = self.__execute_command(command)
        if not stdout:
            raise Exception("Failed to get settings")
        for line in stdout.read().decode().split("\n"):
            if not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key in settings_keys:
                    value = value.replace('"', '')
                    value = True if value == "ON" else False if value == "OFF" else value
                    settings[key] = value
        return settings
    
    def update_settings(self, settings):
        if self.check_artillery_status():
            self.__stop_server()
        current_settings = self.get_settings()

        for key, value in settings.items():
            if key in current_settings and current_settings[key] != value:
                if key in settings_keys:
                    value = "ON" if value is True else "OFF" if value is False else value
                    command = f"sudo sed -i 's/^\\({key}=\\).*/\\1{value}/' /var/artillery/config"
                    _, stderr = self.__execute_command(command)
                    if stderr.read().decode():
                        raise Exception(stderr.read().decode())
                    
    def reset_settings(self):
        return self.update_settings(settings_defaults)
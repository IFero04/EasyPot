import os
from app.services.ssh_service import SSHClientSingleton

class HomeController:
    def __init__(self):
        self.client = SSHClientSingleton()

    def __execute_command(self, command):
        client = self.client.get_client()
        _, stdout, stderr = client.exec_command(command)
        return stdout.read(), stderr.read()
    
    def disconnect(self):
        self.client.disconnect()

    def check_artillery_status(self):
        command = "ps -A x | grep artiller[y]"
        stdout, _ = self.__execute_command(command)
        if "/var/artillery/artillery.py" in stdout.decode():
            return True
        return False

    def get_banned_ips(self):
        command = "cat /var/artillery/banlist.txt"
        stdout, stderr = self.__execute_command(command)
        if stderr:
            raise Exception(stderr.decode())
        banned_ips = stdout.decode().strip().split('\n')
        return [ip for ip in banned_ips if ip and not ip.startswith("#")]

    def start_server(self):
        command = "screen -dmS artillery_run bash -c 'python3 /var/artillery/artillery.py'"
        _, stderr = self.__execute_command(command)
        if stderr:
            raise Exception(stderr)

    def stop_server(self):
        commands = [
            "python3 /var/artillery/kill.py",
            "screen -wipe artillery_run"
        ]
        for command in commands:
            _, stderr = self.__execute_command(command)
            if stderr:
                raise Exception(stderr)
    
    def uninstall_server(self):
        commands = [
            "python3 /var/artillery/uninstall.py",
            "screen -wipe artillery_run"
        ]
        for command in commands:
            _, stderr = self.__execute_command(command)
            if stderr:
                raise Exception(stderr)
    
    def remove_ban(self, ip):
        command = f"sed -i '/{ip}/d' /var/artillery/banlist.txt"
        _, stderr = self.__execute_command(command)
        if stderr:
            raise Exception(stderr.decode())

    def purge_bans(self):
        command = "echo '' > /var/artillery/banlist.txt"
        _, stderr = self.__execute_command(command)
        if stderr:
            raise Exception(stderr.decode()) 


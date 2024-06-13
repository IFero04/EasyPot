import paramiko
from app.services.ssh_service import SSHClientSingleton

class SSHController:
    def __init__(self):
        self.client = SSHClientSingleton()

    def connect(self, hostname, port, username, password):
        result = self.client.connect(hostname, port, username, password)
        if isinstance(result, paramiko.SSHClient):
            return "Connected successfully"
        else:
            return result

    def __execute_command(self, command):
        client = self.client.get_client()
        stdin, stdout, stderr = client.exec_command(command)
        return stdout.read(), stderr.read()

    def disconnect(self):
        self.client.disconnect()
    
    def __create_root_file(self):
        command = "touch /var/artillery_check_root"
        _, stderr = self.__execute_command(command)
        return stderr.strip() == b''
    
    def __remove_root_file(self):
        command = "rm -rf /var/artillery_check_root"
        self.__execute_command(command)

    def is_root(self):
        if self.__create_root_file():
            self.__remove_root_file()
            return True
        return False
    
    def check_installed(self):
        command = "test -d /var/artillery && echo 'installed' || echo 'not_installed'"
        stdout, _ = self.__execute_command(command)
        return stdout.strip() == b'installed'
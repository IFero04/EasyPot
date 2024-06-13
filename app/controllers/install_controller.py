import os
from app.services.ssh_service import SSHClientSingleton

class InstallController:
    def __init__(self):
        self.client = SSHClientSingleton()

    def __execute_command(self, command):
        client = self.client.get_client()
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)
        return stdout.read(), stderr.read()

    def disconnect(self):
        self.client.disconnect()

    def send_file(self):
        current_directory = os.getcwd()
        file_path = os.path.join(current_directory, "app", "static", "zip", "artillery.zip")
        sftp = self.client.get_client().open_sftp()
        remote_path = "/tmp/artillery.zip"
        sftp.put(file_path, remote_path)
        sftp.close()

    def unzip_and_run_setup(self, progress_callback):
        commands = [
            "apt-get install unzip screen -y",
            "rm -rf /tmp/artillery",
            "unzip /tmp/artillery.zip -d /tmp/artillery",
            "rm -rf /tmp/artillery.zip",
            "chmod +x /tmp/artillery/setup.py",
            "python3 /tmp/artillery/setup.py > /tmp/artillery/setup.log 2>&1"
        ]
        total_commands = len(commands)
        completed_commands = 0
        for command in commands:
            stdout, stderr = self.__execute_command(command)
            if stderr:
                print(f"Error executing command '{command}': {stderr}")
                raise Exception(stderr)
            completed_commands += 1
            progress = int(30 + (completed_commands / total_commands) * 60)
            progress_callback(progress)
            print(f"Command '{command}' executed successfully: {stdout}")
        return True

    def check_installed(self, progress_callback):
        commandFolder = "test -d /var/artillery && echo 'installed' || echo 'not_installed'"
        stdoutFolder, _ = self.__execute_command(commandFolder)
        print(f"stdoutFolder: {stdoutFolder}")
        if stdoutFolder.strip() != b'installed':
            raise Exception("Artillery not installed correctly")
        progress_callback(95)
        commandLog = "cat /tmp/artillery/setup.log"
        stdoutLog, stderrLog = self.__execute_command(commandLog)
        if stderrLog:
            raise Exception(stderrLog)
        if stdoutLog.strip() != b'':
            raise Exception("Error during installation")
        progress_callback(100)
        return True

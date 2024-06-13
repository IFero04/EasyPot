import paramiko

class SSHClientSingleton:
    _instance = None
    _client = None
    _channel = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SSHClientSingleton, cls).__new__(cls)
        return cls._instance

    def connect(self, hostname, port, username, password):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                self._client.connect(hostname, port=port, username=username, password=password)
                self._channel = self._client.invoke_shell()
                self._channel.settimeout(0.0)
            except Exception as e:
                self._client = None
                return str(e)
        return self._client

    def get_client(self):
        if self._client is None:
            raise Exception("SSH client is not connected")
        return self._client
    
    def get_channel(self):
        if self._channel is None or self._client is None:
            raise Exception("SSH client is not connected")
        return self._channel

    def disconnect(self):
        if self._client:
            self._client.close()
            self._client = None
            self._channel.close()
            self._channel = None

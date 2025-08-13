import base64
import io
import paramiko
import socket
import time
import logging

LOGGER = logging.getLogger(__name__)

class SFTPConnection:
    def __init__(self, hostname, port, username, ssh_key, ssh_secret, timeout=5):
        self._hostname = hostname
        self._port = int(port)
        self._username = username
        self._ssh_key = ssh_key
        self._ssh_secret = ssh_secret
        self._client = None
        self._transport = None
        self._timeout = timeout

    def connect(self, max_retries=3, retry_delay=5):
        for attempt in range(max_retries):
            try:
                key = base64.b64decode(self._ssh_key).decode("utf-8")
                private_key = paramiko.RSAKey.from_private_key(io.StringIO(key), password=self._ssh_secret)
                self._transport = paramiko.Transport((self._hostname, self._port))
                self._transport.sock.settimeout(self._timeout)
                self._transport.connect(username=self._username, pkey=private_key)
                self._client = paramiko.SFTPClient.from_transport(self._transport)
                LOGGER.info("SFTP Connection established.")
                break
            except Exception as e:
                LOGGER.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise

    def close(self):
        if self._client:
            self._client.close()
        if self._transport:
            self._transport.close()
        LOGGER.info("SFTP connection closed.")

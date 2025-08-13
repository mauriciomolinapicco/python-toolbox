import io
import re
import logging
from .connection import SFTPConnection

LOGGER = logging.getLogger(__name__)

class SFTPService:
    def __init__(self, connection_factory):
        self._factory = connection_factory

    def list_files(self, remote_path, filter_ext=None, prefix=None, regex=None):
        conn = self._factory.create_connection()
        try:
            conn.connect()
            files = conn._client.listdir(remote_path)
            if filter_ext:
                files = [f for f in files if f.endswith(filter_ext)]
            if prefix:
                files = [f for f in files if f.startswith(prefix)]
            if regex:
                pattern = re.compile(regex)
                files = [f for f in files if pattern.fullmatch(f)]
            return files
        finally:
            conn.close()

    def read_file_as_bytesio(self, remote_path):
        conn = self._factory.create_connection()
        conn.connect()
        try:
            with conn._client.open(remote_path, 'rb') as remote_file:
                content = remote_file.read()
            buffer = io.BytesIO(content)
            buffer.name = remote_path.split("/")[-1]
            return buffer
        finally:
            conn.close()

    def upload_fileobj(self, file_obj: io.BytesIO, remote_path: str):
        conn = self._factory.create_connection()
        conn.connect()
        try:
            file_obj.seek(0)
            conn._client.putfo(file_obj, remotepath=remote_path)
            LOGGER.info(f"Archivo subido a SFTP en: {remote_path}")
        finally:
            conn.close()

import requests
import io
import os
import shutil
from utils.compression_utils import compress_folder_to_memory

class Client:
    """
    A client to interact with Synology FileStation API.
    """

    def __init__(self, username, password, server_url, server_port):
        """
        Initialize the Client with authentication details and server information.

        :param username: Synology account username
        :param password: Synology account password
        :param server_url: URL of the Synology server
        :param server_port: Port of the Synology server
        """
        self.username = username
        self.password = password
        self.server_url = server_url
        self.server_port = server_port

    def authenticate(self):
        """
        Authenticate the user and obtain session token and ID.
        """
        auth_url = f"{self.server_url}:{self.server_port}/webapi/auth.cgi"
        auth_params = {
            "api": "SYNO.API.Auth",
            "version": "7",
            "method": "login",
            "account": self.username,
            "passwd": self.password,
            'session': "FileStation",
            "enable_syno_token": "yes",
            "format": "cookie",
        }
        auth_response = requests.get(auth_url, params=auth_params)
        auth_response.raise_for_status()
        auth_data = auth_response.json()
        print(auth_data)
        self.session_token = auth_data["data"]["synotoken"]
        self.session_id = auth_data["data"]["sid"]

    def list_files(self, folder_path):
        """
        List files in the specified folder.

        :param folder_path: Path to the folder to list files from
        """
        files_url = f"{self.server_url}:{self.server_port}/webapi/entry.cgi"
        file_list_params = {
            "api": "SYNO.FileStation.List",
            "method": "list",
            "version": "2",
            "SynoToken": self.session_token,
            "_sid": self.session_id,
            "session": "FileStation",
            "folder_path": folder_path,
        }
        file_list_response = requests.get(files_url, params=file_list_params)
        file_list_response.raise_for_status()
        file_list_data = file_list_response.json()
        return file_list_data

    def download(self, remote_file_path, local_folder_path):
        """
        Download a file from the Synology server to a local folder.

        :param remote_file_path: Path to the remote file on the Synology server
        :param local_folder_path: Path to the local folder to save the file
        :return: Status message
        """
        download_url = f"{self.server_url}:{self.server_port}/webapi/entry.cgi"
        download_params = {
            "api": "SYNO.FileStation.Download",
            "version": "2",
            "method": "download",
            "path": remote_file_path,
            "SynoToken": self.session_token,
            "_sid": self.session_id,
            "session": "FileStation",
        }
        local_file_path = os.path.join(local_folder_path, os.path.basename(remote_file_path))
        download_response = requests.get(download_url, params=download_params, stream=True)
        download_response.raise_for_status()
        with open(local_file_path, 'wb') as local_file:
            shutil.copyfileobj(download_response.raw, local_file)
        return "done"

    def upload_compressed_folder(self, remote_folder, file_path, overwrite="skip", create_parents=False):
        """
        Compress a folder and upload it to the Synology server.

        :param remote_folder: Path to the remote folder on the Synology server
        :param file_path: Path to the local folder to compress and upload
        :param overwrite: Overwrite existing files ("skip" or "overwrite")
        :param create_parents: Create parent directories if they do not exist
        """
        file_path = os.path.normpath(file_path)
        upload_url = f"{self.server_url}:{self.server_port}/webapi/entry.cgi"

        params = {
            "SynoToken": self.session_token,
            "_sid": self.session_id,
            "session": "FileStation",
        }

        data = {
            "api": "SYNO.FileStation.Upload",
            "version": "2",
            "method": "upload",
            "path": remote_folder,
            "create_parents": create_parents,
            "overwrite": overwrite,
        }

        compressed_folder = compress_folder_to_memory(file_path)

        # Define the file and form data
        files = {
            "file": (f"{os.path.basename(file_path)}.zip", io.BufferedReader(compressed_folder), "application/octet-stream")
        }

        # Send the POST request
        try:
            print("Starting upload...")
            upload_response = requests.post(upload_url, 
                                            params=params, 
                                            data=data, 
                                            files=files, 
                                            timeout=60)
            upload_response.raise_for_status()  # Ensure we raise an exception for HTTP errors
            print("Upload successful:", upload_response.json())
        except requests.exceptions.RequestException as e:
            print(f"Upload failed: {e}")
        finally:
            files["file"][1].close()  # Ensure the file is closed
        print("Done")

    def logout(self):
        """
        Logout the user and invalidate the session.
        """
        logout_url = f"{self.server_url}:{self.server_port}/webapi/auth.cgi"
        logout_params = {
            "api": "SYNO.API.Auth",
            "version": "7",
            "method": "logout",
            "session": "FileStation",
            "format": "cookie",
            "SynoToken": self.session_token,
            "_sid": self.session_id,
        }
        logout_response = requests.get(logout_url, params=logout_params)
        logout_response.raise_for_status()
        logout_data = logout_response.json()
        print(logout_data)
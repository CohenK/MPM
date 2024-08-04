import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import io
from utils import helper
from ui.custom_widget_classes import Popup

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveClient:
    def __init__(self, token_file='token.pickle'):
        self.credentials_file = helper.resource_path("utils/client_secret_868314137781-m73562gquoduj597folqfg27qu51f14j.apps.googleusercontent.com.json")
        self.token_file = token_file
        self.creds = self.get_credentials()

    def get_credentials(self):
        creds = None
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def upload_file(self, root, file_path):
        try:
            # Check if file exists
            if not os.path.isfile(file_path):
                print(f"Error: File '{file_path}' does not exist.")
                return None

            service = build('drive', 'v3', credentials=self.creds)
            file_metadata = {'name': os.path.basename(file_path)}
            media = MediaFileUpload(file_path, resumable=True)

            print(f"Uploading file: {file_path}")
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            message = f"File uploaded successfully. File ID: {file.get('id')}"
            Popup(root,message)
            return file.get('id')

        except Exception as e:
            message = f"An error occurred: {e}"
            helper.error_window(message)
            return None
        
    def download_file(self, file_id, dest_path):
            try:
                service = build('drive', 'v3', credentials=self.creds)
                request = service.files().get_media(fileId=file_id)
                fh = io.FileIO(dest_path, 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print(f"Download {int(status.progress() * 100)}%.")
                return dest_path
            except Exception as e:
                print(f"An error occurred: {e}")
                return None
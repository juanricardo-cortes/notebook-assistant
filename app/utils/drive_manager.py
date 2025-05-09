from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import sys
import glob

class GoogleDriveUploader:
    def __init__(self, credentials):
        self.credentials = credentials
        self.drive_service = None

    def authenticate(self):
        if not self.credentials:
            raise Exception("Credentials are required for authentication.")
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    def get_or_create_folder(self, folder_name, parent_id=None):
        """
        Returns the folder ID of 'folder_name' under 'parent_id'.
        If it doesn't exist, creates it.
        """
        query = [
            f"name = '{folder_name}'",
            "mimeType = 'application/vnd.google-apps.folder'",
            "trashed = false"
        ]
        if parent_id:
            query.append(f"'{parent_id}' in parents")
        else:
            query.append("'root' in parents")
        q = " and ".join(query)

        # Search for the folder
        results = self.drive_service.files().list(
            q=q,
            spaces='drive',
            fields="files(id, name)",
            pageSize=1
        ).execute()
        files = results.get('files', [])
        if files:
            return files[0]['id']

        # Folder not found, create it
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            folder_metadata['parents'] = [parent_id]
        folder = self.drive_service.files().create(
            body=folder_metadata,
            fields='id'
        ).execute()
        return folder.get('id')

    def share_with_emails(self, file_id, emails, role='writer'):
        """
        Share the file or folder with a list of emails.
        Args:
            file_id (str): The ID of the file or folder.
            emails (list): List of email addresses.
            role (str): The role to grant ('writer', 'reader', etc.).
        """
        for email in emails:
            permission = {
                'type': 'user',
                'role': role,
                'emailAddress': email
            }
            self.drive_service.permissions().create(
                fileId=file_id,
                body=permission,
                sendNotificationEmail=True,  # Sends an email invite
                fields='id'
            ).execute()

    def upload_file(self, emails_to_share=[]):
        if not self.drive_service:
            raise Exception("You must authenticate first before uploading files.")

        # Step 1: Ensure "Notebook" folder exists in root
        notebook_folder_id = self.get_or_create_folder("Notebook")

        # Step 2: Ensure today's date folder exists inside "Notebook"
        date_today = datetime.now().strftime('%m%d%Y')
        dated_folder_id = self.get_or_create_folder(date_today, parent_id=notebook_folder_id)

        # Step 3: Get latest download file
        downloads_path = self.get_downloads_folder()
        file_path = self.get_latest_download(downloads_path)
        if not file_path:
            raise Exception("No files found in the Downloads folder.")

        # Step 4: Upload file to the dated folder
        file_metadata = {'name': os.path.basename(file_path), 'parents': [dated_folder_id]}
        media = MediaFileUpload(file_path, resumable=True)
        file = self.drive_service.files().create(
            body=file_metadata, media_body=media, fields='id,webViewLink'
        ).execute()

        # Step 5: Share the dated folder with provided emails
        if emails_to_share:
            self.share_with_emails(dated_folder_id, emails_to_share, role='writer')

        print(f"File uploaded successfully. Drive link: {file.get('webViewLink')}")
        return file

    def get_downloads_folder(self):
        if sys.platform == 'win32':
            import winreg
            sub_key = r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                downloads_path = winreg.QueryValueEx(key, downloads_guid)[0]
            return downloads_path
        else:
            return os.path.join(os.path.expanduser('~'), 'Downloads')

    def get_latest_download(self, downloads_path):
        files = glob.glob(os.path.join(downloads_path, '*'))
        if not files:
            return None
        latest_file = max(files, key=os.path.getctime)
        return os.path.abspath(latest_file)

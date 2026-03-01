import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = './allin1/service_account.json'


def authenticate():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    return build('drive', 'v3', credentials=credentials)


def download_folder(service, folder_id, download_path):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType)"
    ).execute()

    items = results.get('files', [])

    for item in items:
        file_id = item['id']
        file_name = item['name']
        mime_type = item['mimeType']

        if mime_type == 'application/vnd.google-apps.folder':
            print(f"Entering folder: {file_name}")
            download_folder(service, file_id, os.path.join(download_path, file_name))
        else:
            print(f"Downloading: {file_name}")
            request = service.files().get_media(fileId=file_id)
            file_path = os.path.join(download_path, file_name)

            with io.FileIO(file_path, 'wb') as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"  {int(status.progress() * 100)}%")

    print("Done.")


if __name__ == '__main__':
    FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH', 'downloaded_files')
    
    if not FOLDER_ID:
        raise ValueError("GOOGLE_DRIVE_FOLDER_ID environment variable is not set. Please check your .env file.")

    service = authenticate()
    download_folder(service, FOLDER_ID, DOWNLOAD_PATH)
import json
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def get_drive_service():
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw:
        raise RuntimeError("Missing GOOGLE_SERVICE_ACCOUNT_JSON secret/environment variable.")
    info = json.loads(raw)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def create_drive_folder_if_missing(service, name, parent_id):
    query = (
        f"mimeType='application/vnd.google-apps.folder' and "
        f"name='{name}' and '{parent_id}' in parents and trashed=false"
    )
    res = service.files().list(q=query, fields="files(id, name)").execute()
    files = res.get("files", [])
    if files:
        return files[0]["id"]

    meta = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    folder = service.files().create(body=meta, fields="id").execute()
    return folder["id"]


def upload_file(local_file, parent_folder_id, drive_filename=None):
    service = get_drive_service()
    filename = drive_filename or os.path.basename(local_file)
    metadata = {"name": filename, "parents": [parent_folder_id]}
    media = MediaFileUpload(local_file, resumable=True)
    uploaded = service.files().create(
        body=metadata,
        media_body=media,
        fields="id, name, webViewLink"
    ).execute()
    print(f"Uploaded: {uploaded.get('name')} -> {uploaded.get('webViewLink')}")
    return uploaded


def upload_file_to_subfolder(local_file, root_folder_id, subfolder_name, drive_filename=None):
    service = get_drive_service()
    subfolder_id = create_drive_folder_if_missing(service, subfolder_name, root_folder_id)
    filename = drive_filename or os.path.basename(local_file)
    metadata = {"name": filename, "parents": [subfolder_id]}
    media = MediaFileUpload(local_file, resumable=True)
    uploaded = service.files().create(
        body=metadata,
        media_body=media,
        fields="id, name, webViewLink"
    ).execute()
    print(f"Uploaded: {uploaded.get('name')} -> {uploaded.get('webViewLink')}")
    return uploaded

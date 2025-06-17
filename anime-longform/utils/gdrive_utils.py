from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from moviepy import VideoFileClip
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

import os
import random
import tempfile

def get_drive_service(service_account_path):
    creds = service_account.Credentials.from_service_account_file(
        service_account_path,
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    return build("drive", "v3", credentials=creds)

def list_files_in_drive(service, folder_id):
    files = []
    page_token = None
    query = f"'{folder_id}' in parents and trashed = false"
    while True:
        response = service.files().list(
            q=query,
            spaces='drive',
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token
        ).execute()
        files.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return files

def download_clips_matching_duration(service_account_path, folder_id, required_duration):
    service = get_drive_service(service_account_path)
    files = list_files_in_drive(service, folder_id)
    random.shuffle(files)

    downloaded_clips = []
    total_duration = 0

    for f in files:
        if not f['mimeType'].startswith("video/"):
            continue

        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        request = service.files().get_media(fileId=f['id'])
        downloader = MediaIoBaseDownload(tmp_file, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        tmp_file.close()

        try:
            clip = VideoFileClip(tmp_file.name)
            if clip.duration + total_duration <= required_duration + 1:
                downloaded_clips.append(clip)
                total_duration += clip.duration
            else:
                clip.close()
                os.remove(tmp_file.name)
        except:
            os.remove(tmp_file.name)

        if total_duration >= required_duration:
            break

    return downloaded_clips
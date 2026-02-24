import requests
import os
import uuid


def extract_file_id(gdrive_link: str):
    # extract file id from standard share link
    parts = gdrive_link.split("/")
    return parts[5]  # works for normal share link


def download_from_gdrive(gdrive_link: str, upload_dir: str):

    file_id = extract_file_id(gdrive_link)

    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = requests.get(download_url)

    if response.status_code != 200:
        raise Exception("Failed to download file from Google Drive")

    filename = f"{uuid.uuid4()}.xlsx"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path
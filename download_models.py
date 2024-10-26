import gdown
import zipfile
import os

# Google Drive file ID
file_id = "1Ho9JjqPukM540JCS2mso_ugfoDPDKfyr"
url = f"https://drive.google.com/uc?id={file_id}"

# Download the file using gdown
gdown.download(url, "yolov3.zip", quiet=False)

# Unzip the file
with zipfile.ZipFile("yolov3.zip", "r") as zip_ref:
    zip_ref.extractall(".")

# Optionally, remove the zip file after extraction
os.remove("yolov3.zip")

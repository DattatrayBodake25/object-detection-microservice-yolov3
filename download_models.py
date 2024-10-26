import requests
import zipfile
import os

url = "https://drive.google.com/uc?export=download&id=1Ho9JjqPukM540JCS2mso_ugfoDPDKfyr"
response = requests.get(url)

# Save the zip file
with open("yolov3.zip", "wb") as f:
    f.write(response.content)

# Unzip the file
with zipfile.ZipFile("yolov3.zip", "r") as zip_ref:
    zip_ref.extractall(".")

# Optionally, remove the zip file after extraction
os.remove("yolov3.zip")

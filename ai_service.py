from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import cv2
import torch
import numpy as np
import sys
import os
from typing import List
import json

# Initialize FastAPI app
app = FastAPI()

# Mount the static folder to serve the HTML file
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add YOLOv3 directory to system path for importing necessary modules
sys.path.append(os.path.join(os.getcwd(), "yolov3"))
from models.common import DetectMultiBackend
from utils.general import non_max_suppression

# Load the YOLOv3 model with specified weights and set to use CPU for inference
weights = 'yolov3/weights/yolov3.pt'  # Ensure this path to the weights file is correct
device = 'cpu'  # Using CPU for inference
model = DetectMultiBackend(weights, device=device)

# Define response model for individual detection result
class Detection(BaseModel):
    label: str
    confidence: float
    bbox: List[int]

# Define response model for all detections in one image
class DetectionResponse(BaseModel):
    detections: List[Detection]

# Store the latest detection results in a global variable for JSON file download
latest_detections = []

# Serve the main HTML interface
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse("static/index.html")

# Object detection endpoint
@app.post("/detect", response_model=DetectionResponse)
async def detect_objects(file: UploadFile = File(...)):
    # Check if a file is uploaded; raise an error if not
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    try:
        # Read and decode the uploaded image into a format usable by OpenCV
        image_bytes = await file.read()
        image = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # Capture original image dimensions
        original_h, original_w = img.shape[:2]

        # Preprocess image: resize to 640x640 for YOLOv3 model requirements
        img_resized = cv2.resize(img, (640, 640))
        img_resized = img_resized.transpose((2, 0, 1))  # Change from HWC to CHW format
        img_resized = np.expand_dims(img_resized, axis=0)  # Add batch dimension
        img_resized = torch.from_numpy(img_resized).float().to(device)  # Convert to tensor and move to device
        img_resized /= 255.0  # Normalize pixel values to [0, 1]

        # Perform object detection
        pred = model(img_resized)
        pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45)

        # Process detection results
        global latest_detections
        latest_detections = []  # Clear previous detections
        if pred[0] is not None and len(pred[0]):
            for det in pred[0]:
                if det is not None and len(det):
                    # Extract bounding box, confidence, and class information
                    box = det[:4]  # Get bounding box coordinates
                    conf = det[4].item()  # Get confidence score
                    cls = int(det[5].item())  # Get class label

                    # Scale bounding box to original image dimensions
                    x1, y1, x2, y2 = (box * torch.tensor([original_w / 640, original_h / 640, original_w / 640, original_h / 640])).int().tolist()

                    latest_detections.append({
                        "label": model.names[cls],
                        "confidence": conf,
                        "bbox": [x1, y1, x2, y2]
                    })

                    # Draw bounding box on original image
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue bounding box

        # Save the output image with bounding boxes drawn
        output_image_path = "output_image.jpg"
        cv2.imwrite(output_image_path, img)

        # Save detections to JSON file
        with open("detections.json", 'w') as json_file:
            json.dump({"detections": latest_detections}, json_file)

        # Return detection results as API response
        return {"detections": latest_detections}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to download the processed image with bounding boxes
@app.get("/download/image")
async def download_image():
    return FileResponse("output_image.jpg", media_type='image/jpeg', filename="output_image.jpg")

# Endpoint to download JSON file with detection results
@app.get("/download/json")
async def download_json():
    # Serve the detections.json file for download
    return FileResponse("detections.json", media_type='application/json', filename="detections.json")

# Run the application (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
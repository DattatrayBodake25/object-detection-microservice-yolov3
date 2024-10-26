# Object Detection Microservice with YOLOv3

This project implements a microservice for object detection using the YOLOv3 model. The application consists of a FastAPI backend that accepts image uploads, performs object detection, and returns the results in JSON format along with an output image containing bounding boxes for detected objects.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Output](#output)
- [Contributing](#contributing)

## Features

- Upload images for object detection
- Process images using the YOLOv3 model
- Display output images with bounding boxes
- Provide detection results in a structured JSON format
- Downloadable output images and JSON data
- Responsive web interface

## Technologies

- **Python**: The programming language used for the backend service.
- **FastAPI**: A modern web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **OpenCV**: Library for computer vision tasks.
- **PyTorch**: Machine learning library for training and inference of neural networks.
- **Docker**: Tool for containerizing the application.
- **HTML/CSS/JavaScript**: Frontend technologies for building the web interface.

## Installation

### Prerequisites

To successfully replicate this solution, ensure you have the following installed:

- Docker: For containerization of the application.
- Python (3.10 or higher): For running the FastAPI application.
- A lightweight object detection model (YOLOv3 in this case). If you don't have a GPU, you can use CPU for inference.

### Clone the Repository

```bash
git clone https://github.com/DattatrayBodake25/object-detection-microservice-yolov3.git
cd object-detection-microservice-yolov3
```

### Install Dependencies
Make sure to install the required Python packages. You can do this by running:
```bash
pip install -r requirements.txt
```

### Usage
Running the Application
You can run the application using the following command:
```bash
uvicorn ai_service:app --host 0.0.0.0 --port 8000
```
Once the server is running, you can access the web interface by navigating to http://127.0.0.1:8000 in your web browser.

### Docker (Optional)
To run the application in a Docker container, you can build and run the container using the following commands:

### Build the Docker image
```bash
docker build -t yolov3-object-detection .
```

### Run the Docker container
```bash
docker run -p 8000:8000 yolov3-object-detection
```
Then access the web interface at
```bash
http://127.0.0.1:8000/static/index.html.
```

### API Endpoints
1. Upload and Detect Objects
Endpoint: /detect
Method: POST
Request: Multipart form-data containing the image file.
Response: JSON object containing detected objects and their bounding boxes.
Example Request:
```bash
curl -X POST "http://127.0.0.1:8000/detect" -F "file=@path_to_your_image.jpg"
```
2. Download Output Image
Endpoint: /download/image
Method: GET
Response: The processed output image with bounding boxes.

3. Download JSON Data
Endpoint: /download/json
Method: GET
Response: A JSON file containing the detection results.

### Testing
You can manually test the object detection functionality by uploading images through the web interface and reviewing the output images and JSON results.

To create testing images, save them in the images for testing directory. This project is set up to handle multiple test images.

### Output
Upon successful detection, the application will generate:

An output image (output_image.jpg) with bounding boxes drawn around detected objects.
A JSON file (detections.json) containing the detection results.

### Example Output Structure

The output JSON structure will look like this:
```bash
{
  "detections": [
    {
      "label": "person",
      "confidence": 0.87,
      "bbox": [100, 50, 200, 300]
    }
  ]
}
```

### Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

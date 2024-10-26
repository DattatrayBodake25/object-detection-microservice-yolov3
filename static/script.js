// Handle form submission for image upload
document.getElementById('upload-form').onsubmit = async function(event) {
    event.preventDefault(); // Prevent default form submission
    const formData = new FormData(); // Create a new FormData object
    formData.append('file', document.getElementById('image').files[0]); // Append the uploaded file

    try {
        // Send the image to the backend for processing
        const response = await fetch('http://127.0.0.1:8000/detect', {
            method: 'POST',
            body: formData // Send the form data
        });

        if (!response.ok) {
            console.error('Error during detection:', response.statusText); // Log error if response is not ok
            return;
        }

        const result = await response.json(); // Parse the JSON response

        // Clear previous results
        const resultContainer = document.getElementById('result');
        resultContainer.innerHTML = '';  // Clear existing content

        // Display processed image from the backend with bounding boxes
        const img = document.createElement('img'); // Create an image element
        img.src = 'http://127.0.0.1:8000/download/image'; // Set image source to the processed image URL
        img.id = 'processed-image'; // Set image ID for reference
        img.onload = function() {
            // Create a canvas overlay on the image
            const canvas = document.createElement('canvas'); // Create a canvas element
            canvas.width = img.width; // Set canvas width to image width
            canvas.height = img.height; // Set canvas height to image height
            const ctx = canvas.getContext('2d'); // Get canvas context for drawing
            ctx.drawImage(img, 0, 0); // Draw the uploaded image on the canvas

            // Filter detections by confidence threshold
            const minConfidence = parseFloat(document.getElementById('min-confidence').value); // Get minimum confidence value
            const detections = result.detections.filter(det => det.confidence >= minConfidence); // Filter detections

            // Loop through detections to draw bounding boxes and labels
            detections.forEach(det => {
                const [x_min, y_min, x_max, y_max] = det.bbox; // Destructure bounding box coordinates

                // Draw bounding box
                ctx.strokeStyle = "red"; // Set stroke color for bounding box
                ctx.lineWidth = 2; // Set line width for bounding box
                ctx.strokeRect(x_min, y_min, x_max - x_min, y_max - y_min); // Draw bounding rectangle

                // Draw label
                ctx.fillStyle = "red"; // Set fill color for label
                ctx.fillText(`${det.label}: ${Math.round(det.confidence * 100)}%`, x_min, y_min > 10 ? y_min - 5 : 10); // Display label with confidence
            });

            // Append the canvas with bounding boxes to the result container
            resultContainer.appendChild(canvas); // Add canvas to the results
        };

        // Append JSON data in a formatted manner below the image
        const pre = document.createElement('pre'); // Create a preformatted text element
        pre.innerText = JSON.stringify(result, null, 2); // Format and display JSON data
        resultContainer.appendChild(pre); // Add JSON to results

        // Add download buttons for the image and JSON data
        const downloadImageBtn = document.createElement('a'); // Create a link element for image download
        downloadImageBtn.href = '/download/image'; // Set href to image download URL
        downloadImageBtn.innerText = 'Download Output Image'; // Set link text
        downloadImageBtn.download = 'output_image.jpg'; // Set filename for download
        resultContainer.appendChild(downloadImageBtn); // Add download button to results

        const downloadJsonBtn = document.createElement('a'); // Create a link element for JSON download
        downloadJsonBtn.href = '/download/json'; // Set href to JSON download URL
        downloadJsonBtn.innerText = 'Download JSON Results'; // Set link text
        downloadJsonBtn.download = 'detections.json'; // Set filename for download
        resultContainer.appendChild(downloadJsonBtn); // Add download button to results

    } catch (error) {
        console.error("An error occurred:", error); // Log any errors
    }
};

// Filter functionality to re-run upload form submission
document.getElementById('filter-btn').onclick = function() {
    document.getElementById('upload-form').onsubmit(); // Re-run the upload form to apply filter
};
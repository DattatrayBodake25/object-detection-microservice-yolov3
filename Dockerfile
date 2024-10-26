# Use a lightweight base image with Python
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Upgrade pip to the latest version and install dependencies in one layer
RUN pip install --upgrade pip && \
    pip install --no-cache-dir torch==2.5.0 torchvision==0.20.0 --find-links https://download.pytorch.org/whl/torch_stable.html

# Copy the requirements file and install any additional dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Create a non-root user and switch to it for better security
RUN useradd -m appuser
USER appuser

# Expose the port your app runs on
EXPOSE 8000

# Command to run your application
CMD ["python", "ai_service.py"]
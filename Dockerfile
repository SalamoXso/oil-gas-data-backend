# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    libavif15 \
    libenchant-2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2 \
    && apt-get clean

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browsers
RUN playwright install

# Copy the rest of the application code
COPY . .

# Expose the port your app runs on
EXPOSE 10000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

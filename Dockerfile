# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Step 1: Update apt-get and install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev

# Step 2: Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 3: Clean up to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Step 4: Copy the application code
COPY . .

# Expose the port for the Flask app
EXPOSE ${PORT:-10000}

# Default command to start the app
CMD ["sh", "start.sh"]

# Dockerfile

# Start with a base Python image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy .env file and load it
COPY .env /app/.env
ENV PORT=10000

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port the app will run on
EXPOSE 10000

# Add a health check for stability
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:$PORT || exit 1

# Start the application
CMD ["./start.sh"]

#!/bin/bash

# Start the scheduler script in the background
echo "Starting scheduler..."
python scheduler.py &

# Start the Flask application and bind to Render's required PORT
echo "Starting Flask app on port ${PORT:-10000}..."
python app.py

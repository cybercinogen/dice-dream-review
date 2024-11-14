#!/bin/bash

# Start the scheduler script in the background
echo "Starting scheduler..."
python scheduler.py &

# Start the Flask application with gunicorn
echo "Starting Flask app with gunicorn on port ${PORT:-10000}..."
gunicorn -w 4 -b 0.0.0.0:${PORT:-10000} app:app

#!/bin/bash

# Start the scheduler in the background
echo "Starting scheduler..."
python scheduler.py &
if [ $? -ne 0 ]; then
    echo "Failed to start scheduler!" >&2
    exit 1
fi

# Start the Flask app
echo "Starting Flask app with gunicorn on port ${PORT:-10000}..."
gunicorn -w 4 -b 0.0.0.0:${PORT:-10000} app:app
if [ $? -ne 0 ]; then
    echo "Failed to start Flask app!" >&2
    exit 1
fi

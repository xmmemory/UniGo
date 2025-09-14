#!/bin/bash
# Start the FastAPI application in production mode

# Activate virtual environment if needed
# source venv/bin/activate

# Run the application using gunicorn
# Use port 8001 to match the development configuration
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8001
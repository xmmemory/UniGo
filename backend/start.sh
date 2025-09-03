#!/bin/bash
# Start the FastAPI application in production mode

# Activate virtual environment if needed
# source venv/bin/activate

# Run the application using gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
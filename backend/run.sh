#!/bin/bash
# Run the FastAPI application

# Activate virtual environment if needed
# source venv/bin/activate

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
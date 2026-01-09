#!/bin/bash

# Startup script for Azure Web App
echo "Starting Interview Evaluation System..."

# Install backend dependencies
cd /home/site/wwwroot
pip install -r requirements.txt

# Install backend-specific dependencies
cd backend
pip install -r requirements.txt

# Start the backend
cd /home/site/wwwroot/backend
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --timeout 300

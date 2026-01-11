#!/bin/bash
set -e

echo "=== Azure Backend Startup ==="
echo "Working directory: $(pwd)"
echo "Python version: $(python --version)"

# Debug: Check environment variables (masked)
echo "AZURE_OPENAI_ENDPOINT: ${AZURE_OPENAI_ENDPOINT:+[SET]}"
echo "AZURE_OPENAI_API_KEY: ${AZURE_OPENAI_API_KEY:+[SET]}"
echo "AZURE_OPENAI_DEPLOYMENT_NAME: ${AZURE_OPENAI_DEPLOYMENT_NAME:+[SET]}"

# Navigate to backend
cd /home/site/wwwroot/backend

# Verify critical files exist
echo "Checking critical files..."
ls -la ../config.yaml 2>/dev/null && echo "config.yaml: OK" || echo "config.yaml: MISSING"
ls -la ../src/graph/graph.py 2>/dev/null && echo "graph.py: OK" || echo "graph.py: MISSING"

# Set Python path to include project root
export PYTHONPATH="/home/site/wwwroot:$PYTHONPATH"

# Start gunicorn with reduced workers for B1 tier
echo "Starting gunicorn..."
gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app \
    --bind 0.0.0.0:8000 \
    --timeout 300 \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --log-level info

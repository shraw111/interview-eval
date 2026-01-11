#!/bin/bash
set -e

echo "=== Azure Backend Startup ==="
echo "Working directory: $(pwd)"
echo "Python version: $(python --version)"

# Debug: Check environment variables (masked)
echo "AZURE_OPENAI_ENDPOINT: ${AZURE_OPENAI_ENDPOINT:+[SET]}"
echo "AZURE_OPENAI_API_KEY: ${AZURE_OPENAI_API_KEY:+[SET]}"
echo "AZURE_OPENAI_DEPLOYMENT_NAME: ${AZURE_OPENAI_DEPLOYMENT_NAME:+[SET]}"

# Get the project root (current directory where Azure extracts)
PROJECT_ROOT=$(pwd)
echo "Project root: $PROJECT_ROOT"

# Verify critical files exist
echo "Checking critical files..."
ls -la "$PROJECT_ROOT/config.yaml" 2>/dev/null && echo "config.yaml: OK" || echo "config.yaml: MISSING"
ls -la "$PROJECT_ROOT/src/graph/graph.py" 2>/dev/null && echo "graph.py: OK" || echo "graph.py: MISSING"
ls -la "$PROJECT_ROOT/backend/app/main.py" 2>/dev/null && echo "main.py: OK" || echo "main.py: MISSING"

# List directory structure for debugging
echo "Directory structure:"
ls -la "$PROJECT_ROOT"

# Set Python path to include project root so 'backend.wsgi' can be imported
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
echo "PYTHONPATH: $PYTHONPATH"

# Start gunicorn with reduced workers for B1 tier
# Use backend.wsgi:application as the entry point
echo "Starting gunicorn..."
gunicorn -w 2 -k uvicorn.workers.UvicornWorker backend.wsgi:application \
    --bind 0.0.0.0:8000 \
    --timeout 300 \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --log-level info

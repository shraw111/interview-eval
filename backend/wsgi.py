"""WSGI entry point for Azure deployment."""
import sys
import os

# Get the directory where wsgi.py is located (backend/)
backend_dir = os.path.dirname(os.path.abspath(__file__))

# Get project root (parent of backend/)
project_root = os.path.dirname(backend_dir)

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Change working directory to backend/
os.chdir(backend_dir)

# Import the FastAPI app
from app.main import app

# This is what gunicorn will import
application = app

"""WSGI entry point for Azure deployment."""
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import the FastAPI app
from backend.app.main import app

# This is what gunicorn will import
application = app

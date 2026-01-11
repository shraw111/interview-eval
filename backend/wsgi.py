"""WSGI entry point for Azure deployment."""
import sys
import os

# Add project root to Python path
# backend/wsgi.py -> backend/ -> project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Change to backend directory for relative imports
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app
from app.main import app

# This is what gunicorn will import
application = app

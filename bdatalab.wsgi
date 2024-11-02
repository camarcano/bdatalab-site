import sys
import os

# Add the app path and virtual environment path
sys.path.insert(0, "/var/www/bdatalab")
sys.path.insert(0, "/var/www/bdatalab/venv/lib/python3.12/site-packages")

from app import create_app
application = create_app()


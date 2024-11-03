# app/routes/streamlit.py
from flask import Blueprint, Response
import streamlit.web.bootstrap as bootstrap
import threading
import requests
import time
import socket
import os

streamlit_bp = Blueprint('streamlit', __name__)


def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def wait_for_streamlit(timeout=30):
    """Wait for Streamlit server to be ready"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_in_use(8501):
            return True
        time.sleep(1)
    return False

def run_streamlit():
    """Run Streamlit server using subprocess"""
    try:
        import subprocess
        app_path = "/opt/bdatalab/repos/BaseballCV/streamlit/annotation_app/app.py"
        venv_python = "/var/www/bdatalab/venv/bin/python"
        
        cmd = [
            venv_python,
            "-m", "streamlit",
            "run",
            app_path,
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(app_path)
        )
        
        print("Started Streamlit server process")
        return process
    except Exception as e:
        print(f"Error starting Streamlit server: {e}")
        raise

# Only start Streamlit if it's not already running
if not is_port_in_use(8501):
    thread = threading.Thread(target=run_streamlit, daemon=True)
    thread.start()
    
    # Wait for Streamlit to start
    if not wait_for_streamlit():
        print("Streamlit server failed to start")
        raise RuntimeError("Streamlit server failed to start")
else:
    logger.info("Streamlit server already running on port 8501")

def proxy_streamlit(path=''):
    """Proxy requests to Streamlit server with error handling"""
    streamlit_url = f'http://localhost:8501/{path}'
    
    try:
        response = requests.get(
            streamlit_url, 
            stream=True,
            timeout=15
        )
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in response.raw.headers.items()
                  if name.lower() not in excluded_headers]
        
        return Response(
            response.content,
            response.status_code,
            headers
        )
    except requests.ConnectionError:
        print(f"Failed to connect to Streamlit server at {streamlit_url}")
        return "Streamlit server is not responding", 503
    except requests.Timeout:
        print(f"Timeout connecting to Streamlit server at {streamlit_url}")
        return "Request to Streamlit server timed out", 504
    except Exception as e:
        print(f"Error proxying request to Streamlit: {e}")
        return f"Internal server error: {str(e)}", 500

@streamlit_bp.route('/annotation_app')
def annotation_app():
    """Serve the Streamlit app"""
    return proxy_streamlit()

@streamlit_bp.route('/annotation_app/<path:path>')
def streamlit_proxy(path):
    """Handle all other Streamlit routes"""
    return proxy_streamlit(path)

# Add health check endpoint
@streamlit_bp.route('/annotation_app/health')
def health_check():
    """Check if Streamlit server is running"""
    if is_port_in_use(8501):
        return "Streamlit server is running", 200
    return "Streamlit server is not running", 503
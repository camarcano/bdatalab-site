# app/routes/streamlit.py
from flask import Blueprint, Response
import streamlit as st
from streamlit.web.bootstrap import run
from streamlit.web.server.server import Server
from streamlit.runtime.scriptrunner import get_script_run_ctx
import threading
import time

streamlit_bp = Blueprint('streamlit', __name__)

def run_streamlit_server():
    """Run Streamlit server in a separate thread"""
    run(
        main_script_path="/opt/bdatalab/repos/BaseballCV/streamlit/annotation_app/app.py",
        command_line=[],
        args=[],
        flag_options={
            'server.port': 8501,
            'server.address': '127.0.0.1',
            'server.headless': True,
            'server.enableCORS': True,
            'server.enableXsrfProtection': False
        }
    )

# Start Streamlit server when blueprint is registered
streamlit_thread = threading.Thread(target=run_streamlit_server, daemon=True)
streamlit_thread.start()

# Wait for Streamlit to start
time.sleep(2)

@streamlit_bp.route('/annotation_app')
def annotation_app():
    """Proxy requests to Streamlit server"""
    import requests
    
    # Forward request to Streamlit
    response = requests.get('http://127.0.0.1:8501')
    
    # Return response with appropriate headers
    return Response(
        response.content,
        status=response.status_code,
        content_type=response.headers['content-type']
    )

# Handle static files and other Streamlit routes
@streamlit_bp.route('/annotation_app/<path:path>')
def streamlit_proxy(path):
    """Proxy all other Streamlit routes"""
    import requests
    
    response = requests.get(f'http://127.0.0.1:8501/{path}')
    
    return Response(
        response.content,
        status=response.status_code,
        content_type=response.headers.get('content-type', 'text/html')
    )
# app/routes/streamlit.py
from flask import Blueprint, render_template, Response
import streamlit as st
from streamlit.web.bootstrap import run
import threading
import requests
from functools import partial

streamlit_bp = Blueprint('streamlit', __name__)

def run_streamlit():
    """Run Streamlit server in a separate thread"""
    run(
        file="/opt/bdatalab/repos/BaseballCV/streamlit/annotation_app/app.py",
        flag_options={
            "server.port": 8501,
            "server.address": "localhost",
            "server.headless": True,
            "server.enableCORS": True,
            "browser.serverAddress": "localhost",
            "server.enableXsrfProtection": False
        }
    )

# Start Streamlit in a separate thread when blueprint is registered
thread = threading.Thread(target=run_streamlit, daemon=True)
thread.start()

def proxy_request(path=''):
    """Proxy requests to Streamlit server"""
    streamlit_url = f'http://localhost:8501/{path}'
    
    try:
        resp = requests.get(streamlit_url, stream=True)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                  if name.lower() not in excluded_headers]
        
        return Response(
            resp.content,
            resp.status_code,
            headers
        )
    except requests.RequestException as e:
        return str(e), 500

@streamlit_bp.route('/annotation_app')
def annotation_app():
    """Main route for Streamlit app"""
    return proxy_request()

@streamlit_bp.route('/annotation_app/<path:path>')
def streamlit_proxy(path):
    """Handle all other Streamlit routes"""
    return proxy_request(path)
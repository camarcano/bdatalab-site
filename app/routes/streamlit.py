from flask import Blueprint, render_template

streamlit_bp = Blueprint('streamlit', __name__)

@streamlit_bp.route('/annotation_app')
def annotation_app():
    """Render the template where Streamlit app will be embedded"""
    return render_template('streamlit/annotation_app.html')

@streamlit_bp.route('/annotation_app/<path:path>')
def streamlit_proxy(path):
    """Render the template where Streamlit app will be embedded for other paths"""
    return render_template('streamlit/annotation_app.html')

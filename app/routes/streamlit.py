from flask import Blueprint, render_template

streamlit_bp = Blueprint('streamlit', __name__)

@streamlit_bp.route('/annotation_app')
def annotation_app():
    return render_template('streamlit/annotation_app.html')

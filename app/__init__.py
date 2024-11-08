import os
from flask import Flask
from .config import config

def create_app(config_name='production'):
    app = Flask(__name__)
    
    # Load configuration from config.py based on environment variable
    config_name = os.environ.get('FLASK_ENV', config_name)
    app.config.from_object(config[config_name])

    # Import and register blueprints
    from .blueprints.admin import admin_bp
    from .blueprints.other_blueprint import other_bp
    from .blueprints.dash_apps import dash_bp, init_dash_apps  # Import Dash apps

    from .routes.main import main_bp
    from .routes.webhook import webhook_bp
    from .routes.streamlit import streamlit_bp


    app.register_blueprint(admin_bp)
    app.register_blueprint(other_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(streamlit_bp)
    app.register_blueprint(dash_bp)  # Register the Dash blueprint

    # Initialize Dash apps
    init_dash_apps(app)

    return app

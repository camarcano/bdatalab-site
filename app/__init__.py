import os
from flask import Flask
from .config import config

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration from config.py based on environment variable
    config_name = os.environ.get('FLASK_ENV', config_name)
    app.config.from_object(config[config_name])

    # Import and register blueprints
    from .blueprints.admin import admin_bp
    from .blueprints.other_blueprint import other_bp
    from .routes.main import main_bp
    from .routes.webhook import webhook_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(other_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(webhook_bp)

    return app

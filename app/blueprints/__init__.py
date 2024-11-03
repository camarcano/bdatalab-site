from flask import Blueprint

# Import blueprints from other modules
from .admin import admin_bp
from .other_blueprint import other_bp

# You can add more blueprints here as needed
# /blueprints/__init__.py
# Add this line to your existing imports
from ..routes.dash import dash_blueprint, init_dash

# In your blueprint registration section, add:
def init_blueprints(app):
    # ... your other blueprint registrations ...
    app.register_blueprint(dash_blueprint, url_prefix='/dash')
    init_dash(app)
    return app
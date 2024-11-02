import os
import logging
from logging.handlers import RotatingFileHandler

# Set up the log file paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, '../logs')
FLASK_LOG_FILE = os.path.join(LOG_DIR, 'flask.log')
DEBUG_LOG_FILE = os.path.join(LOG_DIR, 'debug.log')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        RotatingFileHandler(FLASK_LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5),
        logging.StreamHandler()
    ]
)

# Create a separate handler for debug logs
debug_handler = RotatingFileHandler(DEBUG_LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5)
debug_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
debug_handler.setFormatter(formatter)

# Add the debug handler to the root logger
logging.getLogger().addHandler(debug_handler)

class Config:
    # General Config
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'rickeyhenderson')  # Replace with a secure key in production
    SESSION_COOKIE_SECURE = True

    # Database Config (example with SQLite; replace as needed for production)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///bdatalab.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Static and Media Files Config
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # TailwindCSS Config (if you need additional settings)
    TAILWIND_CDN = "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

# Dictionary to help select the right configuration based on environment
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

# Log Flask application information
app.logger.info("Flask application is starting.")
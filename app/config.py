import os

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

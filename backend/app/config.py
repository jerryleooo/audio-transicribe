import os
import logging
from pathlib import Path

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(BASE_DIR), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Ensure necessary directories exist
    @staticmethod
    def init_app(app):
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Set database URI with absolute path
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
            f'sqlite:////app/instance/dev.db'
        
        # Log to stderr
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        app.logger.addHandler(console_handler)

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    UPLOAD_FOLDER = '/tmp/test_uploads'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)

class ProductionConfig(Config):
    """Production configuration."""
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Set database URI with absolute path
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
            f'sqlite:////app/instance/prod.db'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 
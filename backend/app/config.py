import os
import logging
import pathlib

# Get the absolute path to the project root directory
basedir = pathlib.Path(__file__).parent.parent.absolute()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development')
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
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
        
        # Use relative path for local development
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_URL') or \
            f'sqlite:///{os.path.join(basedir, "instance", "dev.db")}'
        
        # Log to stderr
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        app.logger.addHandler(console_handler)

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///:memory:'
    UPLOAD_FOLDER = '/tmp/test_uploads'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)

class ProductionConfig(Config):
    """Production configuration."""
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Use absolute path for Docker environment
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
            'sqlite:////app/instance/prod.db'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 
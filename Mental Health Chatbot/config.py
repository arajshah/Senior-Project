import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///mental_health.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-never-use-in-production')
    
    # DeepSeek Configuration
    DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'http://localhost:11434/v1/complete')
    DEEPSEEK_MAX_TOKENS = 150
    DEEPSEEK_TEMPERATURE = 0.7
    DEEPSEEK_TOP_P = 0.9

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
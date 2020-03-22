class BaseConfig(object):
    """Base configuration"""

    JSON_AS_ASCII = False

class DevelopmentConfig(BaseConfig):
    """Production configuration"""
    
    ENV = 'dev'
    DEBUG = True
    SECRET_KEY = 'djskla'
class BaseConfig(object):
    """Base configuration"""

    JSON_AS_ASCII = False

class DevelopmentConfig(BaseConfig):
    """Production configuration"""
    
    ENV = 'dev'
    DEBUG = True
    SECRET_KEY = 'djskla'

    MONGO_URI = 'mongodb://49.232.5.176:34541/dev'
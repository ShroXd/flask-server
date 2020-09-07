PASSWORD_KEY = 'WEOIEuOz0Kra1qQwlNI0Cx54'


class BaseConfig(object):
    """Base configuration"""

    JSON_AS_ASCII = False
    TOKEN_EXPIRES = 60 * 60 * 24 * 7


class DevelopmentConfig(BaseConfig):
    """Production configuration"""
    
    ENV = 'dev'
    DEBUG = True
    SECRET_KEY = 'djskla'

    MONGO_URI = 'mongodb://49.232.5.176:34541/dev'


class TestConfig(BaseConfig):
    """Production configuration"""

    ENV = 'test'
    DEBUG = True
    SECRET_KEY = 'djskla'

    MONGO_URI = 'mongodb://49.232.5.176:34541/test'

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'thisisasecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'thisisasecretkey'
    
class TestingConfig(Config):
    TESTING = True







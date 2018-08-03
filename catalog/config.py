import os


class Config:
    DEBUG = False
    TESTING = False
    DATABASE = "sqlite://{}".format(os.path.join(os.path.abspath(os.path.dirname(__file__)), "/db/catalog.db"))


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

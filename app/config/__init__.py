from dotenv import load_dotenv
from pathlib import Path
import os

basedir = os.path.abspath(Path(__file__).parents[2])
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')  # Añadido por seguridad
    
    @staticmethod
    def init_app(app):
        pass

class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Prioriza TEST_DATABASE_URI si está en .env, sino usa sqlite por defecto
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI', 'sqlite:///test.db')

class DevelopmentConfig(Config):
    TESTING = False
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///development.db')

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

def factory(app: str) -> Config:
    configuration = {
        'testing': TestConfig,
        'development': DevelopmentConfig,
        'production': ProductionConfig
    }
    
    return configuration[app]
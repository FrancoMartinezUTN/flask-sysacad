# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import factory
import os
import logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    env = os.environ.get('FLASK_CONTEXT', 'development')
    config = factory(env.lower())
    app.config.from_object(config)
    
    db.init_app(app)
    
    from app.routes.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Importar y registrar comandos dinámicamente
    with app.app_context():
        from .cli import register_commands
        register_commands(app)
    
    with app.app_context():
        db.create_all()
    
    return app

__all__ = ['db']
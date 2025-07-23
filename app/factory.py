from flask import Flask
from app.db import db
from app.config.entornos import get_config

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)

    
    import app.models

    return app
import os
from flask import Flask
from app.db import db

def create_app():
    app = Flask(__name__)

    context = os.getenv('FLASK_CONTEXT', 'development')

    from app.config.entornos import factory
    app.config.from_object(factory(context))

    # Config por si no viene de factory
    if "SQLALCHEMY_DATABASE_URI" not in app.config:
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://camila:Camila2025@localhost:5432/sysacaddb"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar db con Flask
    db.init_app(app)

    # Registrar modelos
    from app import models  

    # Registrar blueprints
    from app.routes.alumno_routes import alumno_bp
    from app.routes.materia_routes import materia_bp
    app.register_blueprint(alumno_bp)
    app.register_blueprint(materia_bp)

    # Registrar comandos CLI
    from app.cli import register_cli
    register_cli(app)

    return app

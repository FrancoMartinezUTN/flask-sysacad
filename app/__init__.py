import os
from flask import Flask
from app.db import db

def create_app():
    app = Flask(__name__)

    
    context = os.getenv('FLASK_CONTEXT', 'development')

    from app.config.entornos import factory
    app.config.from_object(factory(context))

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar blueprints
    from app.routes.alumno_routes import alumno_bp
    from app.routes.materia_routes import materia_bp
    app.register_blueprint(alumno_bp)
    app.register_blueprint(materia_bp)

    # Registrar comandos CLI personalizados
    from app.cli import register_cli
    register_cli(app)

    return app

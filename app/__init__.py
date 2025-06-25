import os
from flask import Flask
from dotenv import load_dotenv

# Cargar las variables desde .env
load_dotenv()

# Importar la base de datos desde el módulo db.py
from app.db import db

def create_app():
    app = Flask(__name__)

    # Obtener el contexto desde .env
    context = os.getenv('FLASK_CONTEXT', 'development')

    # Importar clase de configuración correspondiente
    from app.config.entornos import factory
    app.config.from_object(factory(context))

    # Inicializar la DB
    db.init_app(app)

    # Importar rutas (blueprints)
    from app.routes.alumno_routes import alumno_bp
    from app.routes.materia_routes import materia_bp

    app.register_blueprint(alumno_bp)
    app.register_blueprint(materia_bp)

    return app

# Exportamos los elementos necesarios al importar app
__all__ = ["create_app", "db"]

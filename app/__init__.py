import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar las variables desde .env
load_dotenv()

# Base de datos
db = SQLAlchemy()

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
    app.register_blueprint(alumno_bp)

    return app

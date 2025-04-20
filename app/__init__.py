from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Inicializamos la extensión de SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Cargar variables desde el archivo .env
    load_dotenv()

    # Crear la instancia de la app
    app = Flask(__name__)

    # Configurar la app usando el archivo config.py
    app.config.from_object('config.Config')

    # Inicializar la base de datos con la app
    db.init_app(app)

    # Importar y registrar los blueprints (rutas)
    from app.routes.alumno_routes import alumno_bp
    app.register_blueprint(alumno_bp)

    return app

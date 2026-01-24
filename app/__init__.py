import os
from flask import Flask
from dotenv import load_dotenv
from app.db import db, migrate


def create_app():
    """
    Factory de la app Flask.
    Carga configuración desde variables de entorno y registra extensiones/rutas.
    """

    # En uso normal cargamos .env; en los tests podemos saltarlo con FLASK_SKIP_DOTENV=1
    if os.getenv("FLASK_SKIP_DOTENV", "0") != "1":
        load_dotenv()  # lee .env en la raíz del proyecto

    app = Flask(__name__)

    # --- Configuración de base de datos ---
    uri = os.getenv("SQLALCHEMY_DATABASE_URI")

    # Fallback para entorno de desarrollo SOLO si SQLALCHEMY_DATABASE_URI no está definida
    if not uri:
        ctx = os.getenv("FLASK_CONTEXT", "development").lower()
        if ctx in ("development", "dev"):
            uri = os.getenv("DEV_DATABASE_URI", "sqlite:///sysacad_dev.db")

    if not uri:
        raise RuntimeError("No hay cadena de conexión. Definí SQLALCHEMY_DATABASE_URI en .env")

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Manejo seguro de SECRET_KEY ---
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY no definida en variables de entorno")

    # --- Inicialización de extensiones ---
    db.init_app(app)
    migrate.init_app(app, db)

    # --- Registro de blueprints ---
    from app.routes.alumno_routes import alumno_bp
    app.register_blueprint(alumno_bp)

    return app

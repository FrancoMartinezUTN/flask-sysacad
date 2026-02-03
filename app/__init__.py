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

    # Detectar contexto de ejecución
    ctx = os.getenv("FLASK_CONTEXT", "development").lower()

    # --- Configuración de base de datos ---
    uri = os.getenv("SQLALCHEMY_DATABASE_URI")

    if not uri:
        if ctx == "testing":
            # En testing: priorizar TEST_DATABASE_URI, luego fallback a SQLite en memoria
            uri = os.getenv("TEST_DATABASE_URI", "sqlite:///:memory:")
        elif ctx in ("development", "dev"):
            # En development: priorizar DEV_DATABASE_URI, luego fallback a SQLite file
            uri = os.getenv("DEV_DATABASE_URI", "sqlite:///sysacad_dev.db")

    # En production (u otro contexto) sin URI: fallar explícitamente
    if not uri:
        raise RuntimeError("No hay cadena de conexión. Definí SQLALCHEMY_DATABASE_URI en .env")

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Configuración específica de testing ---
    if ctx == "testing":
        app.config["TESTING"] = True

    # --- Manejo seguro de SECRET_KEY ---
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        if ctx == "testing":
            # En testing permitimos un fallback para no requerir .env
            secret_key = "test-secret-key-not-for-production"
        else:
            raise RuntimeError("SECRET_KEY no definida en variables de entorno")
    app.config["SECRET_KEY"] = secret_key

    # --- Inicialización de extensiones ---
    db.init_app(app)
    migrate.init_app(app, db)

    # --- Registro de blueprints ---
    from app.routes.alumno_routes import alumno_bp
    app.register_blueprint(alumno_bp)

    return app

import os
from flask import Flask
from dotenv import load_dotenv
from app.db import db

def create_app():
    load_dotenv()  # lee .env en la raíz
    app = Flask(__name__)

    uri = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not uri:
        # fallback por contexto (opcional)
        ctx = (os.getenv("FLASK_CONTEXT") or "development").lower()
        if ctx in ("development", "dev"):
            uri = os.getenv("DEV_DATABASE_URI", "sqlite:///sysacad_dev.db")

    if not uri:
        raise RuntimeError("No hay cadena de conexión. Definí SQLALCHEMY_DATABASE_URI en .env")

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    db.init_app(app)

    # registra blueprints que ya existan
    from app.routes.alumno_routes import alumno_bp
    app.register_blueprint(alumno_bp)

    return app

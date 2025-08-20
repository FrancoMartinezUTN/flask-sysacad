import pytest
from app import create_app
from app.db import db

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://camila:Camila2025@localhost:5432/sysacaddb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture()
def app():
    app = create_app()
    with app.app_context():
        # Opcional: limpiar tablas antes de tests
        db.drop_all()
        db.create_all()
        yield app
        # Limpiar al finalizar
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

import os
import pytest
from app import create_app, db
from app.repositories.grado_repositorio import insertar_grado

@pytest.fixture
def app_context():
    os.environ["FLASK_CONTEXT"] = "testing"
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_insertar_grado(app_context):
    from app.models import Grado
    insertar_grado(1, "Test Grado")
    grado = db.session.get(Grado, 1)  # Cambiar de Grado.query.get(1)
    assert grado is not None
    assert grado.nombre == "Test Grado"
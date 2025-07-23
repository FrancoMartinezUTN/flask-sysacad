import os
import pytest
from app import create_app, db
from app.repositories.facultad_repositorio import insertar_facultad

@pytest.fixture
def app_context():
    os.environ["FLASK_CONTEXT"] = "testing"
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_insertar_facultad(app_context):
    from app.models import Facultad
    insertar_facultad(1, "Facultad de Ingeniería")
    facultad = db.session.get(Facultad, 1)  # Cambiar de Facultad.query.get(1)
    assert facultad is not None
    assert facultad.nombre == "Facultad de Ingeniería"
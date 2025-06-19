import os
import pytest
from app import create_app, db
from app.models.facultad import Facultad
from app.importers.facultades_importer import parse_facultades
from app.repositories.facultades_repositorio import insertar_o_actualizar_facultad

@pytest.fixture
def app_context():
    os.environ["FLASK_CONTEXT"] = "testing"
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_importar_facultades_desde_xml_real(app_context):
    ruta = "archivados_xml/facultades.xml"
    facultades = parse_facultades(ruta)

    for f in facultades:
        insertar_o_actualizar_facultad(f["id"], f["nombre"])

    todos = Facultad.query.all()
    assert len(todos) == len(facultades)
    assert any("Facultad" in f.nombre for f in todos)
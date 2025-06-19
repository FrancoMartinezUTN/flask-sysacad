import os
import pytest
from app import create_app, db
from app.models.universidad import Universidad
from app.importers.universidad_importer import parse_universidades
from app.repositories.universidad_repositorio import insertar_o_actualizar_universidad

@pytest.fixture
def app_context():
    os.environ["FLASK_CONTEXT"] = "testing"
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_importar_universidades_desde_xml_real(app_context):
    ruta = "archivados_xml/universidad.xml"
    universidades = parse_universidades(ruta)

    for u in universidades:
        insertar_o_actualizar_universidad(u["id"], u["nombre"])

    todos = Universidad.query.all()
    assert len(todos) == len(universidades)
    assert any("Universidad" in u.nombre for u in todos)

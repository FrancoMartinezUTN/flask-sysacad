import tempfile
import os
import pytest
from app import create_app, db
from app.models.grado import Grado
from app.importers.grados_importer import parse_grados
from app.repositories.grado_repositorio import insertar_o_actualizar_grado


XML_EJEMPLO = """
<grados>
<grado>
    <id>10</id>
    <nombre>Grado Técnico</nombre>
</grado>
<grado>
    <id>20</id>
    <nombre>Grado Universitario</nombre>
</grado>
</grados>
"""

@pytest.fixture
def app_context():
    os.environ["FLASK_CONTEXT"] = "testing"
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_parse_grados():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode="w", encoding="windows-1252") as f:
        f.write(XML_EJEMPLO)
        xml_path = f.name

    try:
        grados = parse_grados(xml_path)
        assert len(grados) == 2
        assert grados[0]["id"] == 10
        assert grados[0]["nombre"] == "Grado Técnico"
        assert grados[1]["nombre"] == "Grado Universitario"
    finally:
        os.remove(xml_path)

def test_insertar_grados(app_context):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode="w", encoding="windows-1252") as f:
        f.write(XML_EJEMPLO)
        xml_path = f.name

    try:
        grados = parse_grados(xml_path)
        with app_context.app_context():
            for g in grados:
                insertar_o_actualizar_grado(g['id'], g['nombre'])
            db.session.commit()

            lista = Grado.query.order_by(Grado.id).all()
            assert len(lista) == 2
            assert lista[0].id == 10
            assert lista[0].nombre == "Grado Técnico"
            assert lista[1].nombre == "Grado Universitario"
    finally:
        os.remove(xml_path)

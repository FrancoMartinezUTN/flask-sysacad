import tempfile
import os
import pytest
from app import create_app, db
from app.models.grado import Grado
from app.importers.grados_importer import parse_grados

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

def test_parse_grados(app_context):
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

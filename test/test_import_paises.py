import tempfile
import os
import pytest
from app import create_app, db
from app.models.pais import Pais  # ✅ Importación directa y correcta
from app.services.import_service import importar_paises

XML_EJEMPLO = """
<paises>
  <pais>
    <id>100</id>
    <nombre>Testlandia</nombre>
  </pais>
  <pais>
    <id>200</id>
    <nombre>Demoamérica</nombre>
  </pais>
</paises>
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

def test_importar_paises(app_context):
    # Crear archivo XML temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode="w", encoding="windows-1252") as f:
        f.write(XML_EJEMPLO)
        xml_path = f.name

    try:
        importar_paises(xml_path)

        paises = Pais.query.all()
        assert len(paises) == 2

        nombres = [p.nombre for p in paises]
        assert "Testlandia" in nombres
        assert "Demoamérica" in nombres

    finally:
        os.remove(xml_path)

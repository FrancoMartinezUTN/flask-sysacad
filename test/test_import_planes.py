import os
import tempfile
import pytest
from app import create_app, db
from app.models import Plan
from app.services.import_service import importar_planes

XML_EJEMPLO = """
<planes>
  <plan>
    <id>1</id>
    <nombre>Ingeniería en Sistemas</nombre>
  </plan>
  <plan>
    <id>2</id>
    <nombre>Ingeniería Industrial</nombre>
  </plan>
</planes>
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

def test_importar_planes(app_context):
    # Usamos UTF-8 para evitar problemas con caracteres como "í"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode="w", encoding="utf-8") as f:
        f.write(XML_EJEMPLO)
        xml_path = f.name

    try:
        importar_planes(xml_path)
        planes = Plan.query.all()
        assert len(planes) == 2
        assert any(p.nombre == "Ingeniería en Sistemas" for p in planes)
        assert any(p.nombre == "Ingeniería Industrial" for p in planes)
    finally:
        os.remove(xml_path)

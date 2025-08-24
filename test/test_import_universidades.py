import os
import tempfile
import pytest
from app import create_app, db
from app.models.universidad import Universidad
from app.importers.universidades_importer import parse_universidades
from app.repositories.universidad_repositorio import insertar_o_actualizar_universidad

XML_EJEMPLO = """
<universidades>
  <universidad>
    <id>1</id>
    <nombre>Universidad Nacional de Cuyo</nombre>
  </universidad>
  <universidad>
    <id>2</id>
    <nombre>Universidad Tecnológica Nacional</nombre>
  </universidad>
</universidades>
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

def test_parse_e_insertar_universidades(app_context):
    # Crear XML temporal para una prueba auto-contenida
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".xml", mode="w", encoding="windows-1252"
    ) as f:
        f.write(XML_EJEMPLO)
        xml_path = f.name

    try:
        universidades = parse_universidades(xml_path)
        for u in universidades:
            insertar_o_actualizar_universidad(u["id"], u["nombre"])

        all_universidades = Universidad.query.all()
        assert len(all_universidades) == 2
        assert any(u.nombre == "Universidad Nacional de Cuyo" for u in all_universidades)
        assert any(u.nombre == "Universidad Tecnológica Nacional" for u in all_universidades)
    finally:
        os.remove(xml_path)

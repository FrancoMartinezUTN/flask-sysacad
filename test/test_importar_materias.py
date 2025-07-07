from app import create_app, db
from app.models import Materia  # Asegurate de que esté bien importado
from scripts.importar_materias import importar_materias_desde_xml

import os
import pytest

@pytest.fixture
def app_context():
    os.environ["FLASK_CONTEXT"] = "testing"
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_importar_materias(app_context):
    ruta_archivo = "scripts/materias.xml"  # esta ruta es relativa a el archivo que está en esa carpeta dentro del proyecto
    importar_materias_desde_xml(ruta_archivo)

    materias = Materia.query.all()
    print(f"Se importaron {len(materias)} materias.")
    assert len(materias) > 0

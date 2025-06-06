import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.importers.universidades_importer import parse_universidades
from app.repositories.universidad_repositorio import insertar_universidad


os.environ["FLASK_CONTEXT"] = "development"
app = create_app()

XML_PATH = "archivados_xml/universidades.xml"

with app.app_context():
    universidades = parse_universidades(XML_PATH)
    for u in universidades:
        insertar_universidad(u["id"], u["nombre"])
    print(f"✅ Se importaron {len(universidades)} universidades.")

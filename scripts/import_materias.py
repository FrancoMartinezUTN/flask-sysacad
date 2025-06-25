
import os
import xml.etree.ElementTree as ET
from app import create_app, db
from app.models import Materia

def importar_materias(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for materia_elem in root.findall("materia"):
        codigo = materia_elem.find("codigo").text.strip()
        nombre = materia_elem.find("nombre").text.strip()

        if not db.session.query(Materia).filter_by(codigo=codigo).first():
            nueva_materia = Materia(codigo=codigo, nombre=nombre)
            db.session.add(nueva_materia)
            print(f"✔️ Materia agregada: {codigo} - {nombre}")
        else:
            print(f"⏭️ Ya existe: {codigo} - {nombre}")

    db.session.commit()
    print("✅ Importación finalizada.")

if __name__ == "__main__":
    os.environ["FLASK_CONTEXT"] = "development"
    app = create_app()
    with app.app_context():
        importar_materias("scripts/materias.xml")

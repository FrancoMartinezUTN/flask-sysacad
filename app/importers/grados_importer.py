import os
import sys
import xml.etree.ElementTree as ET
from app.repositories.grado_repositorio import insertar_grado
from app.repositories.materia_repositorio import insertar_materia
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def importar_grados_desde_xml(path_xml, app=None):
    if app is None:
        from flask import current_app as app
    with app.app_context():
        try:
            logging.info("📦 Procesando archivo: %s", path_xml)
            tree = ET.parse(path_xml)
            root = tree.getroot()

            for elem in root.findall(".//Grado"):
                nombre = elem.find("Nombre").text.strip()
                insertar_grado(nombre=nombre)

            for elem in root.findall(".//Materia"):
                nombre = elem.find("Nombre").text.strip()
                grado_id = int(elem.find("GradoId").text.strip())
                insertar_materia(nombre, grado_id)

            logging.info("✅ Importación de grados y materias finalizada.")

        except Exception as e:
            logging.error("❌ Error al importar grados o materias: %s", e)

if __name__ == "__main__":
    ejemplo_xml = "materias_ejemplo.xml"
    importar_grados_desde_xml(ejemplo_xml)
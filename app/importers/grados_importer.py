# app/importers/grados_importer.py
import os
import sys
import xml.etree.ElementTree as ET
from app.repositories.grado_repositorio import insertar_grado
import logging

# Añadir la carpeta raíz del proyecto al sys.path (por si acaso)
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

            logging.info("✅ Importación de grados finalizada.")

        except Exception as e:
            logging.error("❌ Error al importar grados: %s", e)

if __name__ == "__main__":
    ejemplo_xml = "grados_ejemplo.xml"
    importar_grados_desde_xml(ejemplo_xml)
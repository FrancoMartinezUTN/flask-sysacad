import xml.etree.ElementTree as ET
from app.repositories.plan_repositorio import insertar_plan

def parsear_planes(path_xml):
    tree = ET.parse(path_xml, parser=ET.XMLParser(encoding='utf-8'))
    root = tree.getroot()

    for nodo in root.findall("plan"):
        id_ = int(nodo.find("id").text)
        nombre = nodo.find("nombre").text.strip()
        insertar_plan(id_, nombre)

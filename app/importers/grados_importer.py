# TODO: implementar parser para grados.xml
import xml.etree.ElementTree as ET

def parse_grados(xml_path: str):
    tree = ET.parse(xml_path, parser=ET.XMLParser(encoding='windows-1252'))
    root = tree.getroot()
    # retornar lista de dicts con id y nombre, por ejemplo
    return []

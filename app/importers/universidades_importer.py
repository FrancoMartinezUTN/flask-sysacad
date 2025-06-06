import xml.etree.ElementTree as ET

def parse_universidades(xml_path: str):
    tree = ET.parse(xml_path, parser=ET.XMLParser(encoding='windows-1252'))
    root = tree.getroot()

    return [{
        'id': int(elem.find('id').text),
        'nombre': elem.find('nombre').text.strip()
    } for elem in root.findall('universidad')]

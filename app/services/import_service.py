from app.importers.paises_importer import parse_paises
from app.repositories.pais_repository import insertar_pais
from app.importers.planes_importer import parsear_planes

def importar_paises(xml_path):
    paises = parse_paises(xml_path)
    for pais in paises:
        insertar_pais(pais['id'], pais['nombre'])

def importar_planes(path):
    parsear_planes(path)

from app.importers.paises_importer import parse_paises
from app.repositories.pais_repositorio import insertar_pais

def importar_paises(xml_path):
    paises = parse_paises(xml_path)
    for pais in paises:
        insertar_pais(pais['id'], pais['nombre'])

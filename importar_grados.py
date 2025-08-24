from app import create_app, db
from app.importers.grados_importer import parse_grados
from app.repositories.grado_repositorio import insertar_o_actualizar_grado, guardar_cambios

def importar_desde_xml(ruta_xml):
    app = create_app()
    with app.app_context():
        grados = parse_grados(ruta_xml)
        for g in grados:
            insertar_o_actualizar_grado(g['id'], g['nombre'])
        guardar_cambios()
        print(f"Se importaron {len(grados)} grados desde {ruta_xml}")

if __name__ == "__main__":
    ruta_xml = "grados.xml" 
    importar_desde_xml(ruta_xml)

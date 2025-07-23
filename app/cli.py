# app/cli.py
import click
from app.importers.grados_importer import importar_grados_desde_xml

def register_commands(app):
    @app.cli.command("importar_grados")
    @click.argument("archivo")
    def importar_grados(archivo):
        """Importa grados desde un archivo XML."""
        importar_grados_desde_xml(archivo, app)

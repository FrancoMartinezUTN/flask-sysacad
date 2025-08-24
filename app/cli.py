import click
from flask import Flask
from app.importers.importar_alumnos import importar_alumnos_csv

def register_cli(app: Flask):
    @app.cli.command("importar")
    @click.argument("tipo")
    @click.argument("archivo")
    def importar(tipo, archivo):
        """
        Importa datos al sistema.

        Uso:
        flask importar alumnos alumnos.csv
        """
        if tipo == "alumnos":
            importar_alumnos_csv(archivo)
        else:
            click.echo(f"❌ Tipo de importación no reconocido: {tipo}")

from app.models.materia import Materia
from app import db

def crear_materia(data):
    nombre = data.get('nombre')
    codigo = data.get('codigo')
    anio = data.get('anio')

    if not nombre or not codigo or not anio:
        raise ValueError("Los campos 'nombre', 'codigo' y 'anio' son obligatorios.")

    nueva_materia = Materia(nombre=nombre, codigo=codigo, anio=anio)
    db.session.add(nueva_materia)
    db.session.commit()
    return nueva_materia.to_dict()

def obtener_materias():
    materias = Materia.query.all()
    return [materia.to_dict() for materia in materias]

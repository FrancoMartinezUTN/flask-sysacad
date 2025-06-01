from app import db
from app.models.materia import Materia

def obtener_materias():
    return [materia.to_dict() for materia in Materia.query.all()]

def crear_materia(data):
    nueva_materia = Materia(
        nombre=data.get('nombre'),
        anio=data.get('anio')
    )
    db.session.add(nueva_materia)
    db.session.commit()
    return nueva_materia.to_dict()

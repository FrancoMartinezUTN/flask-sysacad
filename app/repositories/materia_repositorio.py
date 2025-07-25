from app import db
from app.models.materia import Materia

def insertar_materia(nombre, grado_id):
    materia = Materia(nombre=nombre, grado_id=grado_id)
    db.session.add(materia)
    db.session.commit()
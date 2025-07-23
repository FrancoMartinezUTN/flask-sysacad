from app import db
from app.models import Facultad

def insertar_facultad(id, nombre):
    nueva_facultad = Facultad(id=id, nombre=nombre)
    db.session.add(nueva_facultad)
    db.session.commit()
from app import db
from app.models.facultad import Facultad

def insertar_o_actualizar_facultad(id, nombre):
    if not db.session.get(Facultad, id):
        nueva = Facultad(id=id, nombre=nombre)
        db.session.add(nueva)
        db.session.commit()

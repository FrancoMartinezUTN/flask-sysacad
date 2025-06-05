from app import db
from app.models.grado import Grado

def insertar_grado(id, nombre):
    if not db.session.get(Grado, id):
        nuevo = Grado(id=id, nombre=nombre)
        db.session.add(nuevo)
        db.session.commit()
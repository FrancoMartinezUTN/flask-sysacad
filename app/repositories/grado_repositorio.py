from app import db
from app.models.grado import Grado

def insertar_o_actualizar_grado(id, nombre):
    grado = db.session.get(Grado, id)
    if grado:
        return grado  
    nuevo_grado = Grado(id=id, nombre=nombre)
    db.session.add(nuevo_grado)
    return nuevo_grado

def guardar_cambios():
    db.session.commit()

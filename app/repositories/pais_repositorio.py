from app import db
from app.models.pais import Pais  

def insertar_pais(id, nombre):
    if not db.session.get(Pais, id):
        nuevo_pais = Pais(id=id, nombre=nombre)
        db.session.add(nuevo_pais)
        db.session.commit()

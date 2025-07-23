# app/repositories/grado_repositorio.py
from app import db
from app.models import Grado

def insertar_grado(nombre):
    grado = Grado(nombre=nombre)
    db.session.add(grado)
    db.session.commit()
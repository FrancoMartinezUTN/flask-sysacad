from app import db  
from app.models import Plan

def insertar_plan(id, nombre):
    if not db.session.get(Plan, id):
        nuevo = Plan(id=id, nombre=nombre)
        db.session.add(nuevo)
        db.session.commit()

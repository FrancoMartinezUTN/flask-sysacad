from app import db
from app.models.universidad import Universidad

def insertar_o_actualizar_universidad(id, nombre):
    if not db.session.get(Universidad, id):
        nueva = Universidad(id=id, nombre=nombre)
        db.session.add(nueva)
        db.session.commit()

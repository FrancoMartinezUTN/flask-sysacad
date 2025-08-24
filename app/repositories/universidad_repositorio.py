from app.db import db
from app.models.universidad import Universidad

def insertar_o_actualizar_universidad(id: int, nombre: str):
    """
    Crea o actualiza una Universidad por clave primaria (id).
    - Si existe, actualiza 'nombre'.
    - Si no existe, crea el registro.
    """
    obj = db.session.get(Universidad, id)  # busca por PK de forma directa y eficiente
    if obj is None:
        obj = Universidad(id=id, nombre=nombre)
        db.session.add(obj)
    else:
        obj.nombre = nombre

    db.session.commit()
    return obj

# Mantener compatibilidad con el nombre antiguo (si otras partes lo llaman)
def insertar_universidad(id: int, nombre: str):
    return insertar_o_actualizar_universidad(id, nombre)

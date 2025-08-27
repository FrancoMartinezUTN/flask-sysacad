from app.db import db
from app.models.alumno import Alumno

def get_alumnos():
    return [a.to_dict() for a in Alumno.query.all()]

def create_alumno(data):
    a = Alumno(
        legajo=data.get("legajo"),          
        nombre=data["nombre"],
        apellido=data["apellido"],
        dni=data["dni"],
        email=data["email"],
        facultad=data.get("facultad"),         
        fecha_nacimiento=data.get("fecha_nacimiento"),
        carrera=data.get("carrera"),
        anio_ingreso=data.get("anio_ingreso"),
    )
    db.session.add(a)
    db.session.commit()
    return a.to_dict()

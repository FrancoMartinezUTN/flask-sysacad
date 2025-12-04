from app.db import db
from app.models.alumno import Alumno


def get_alumnos():
    """
    Devuelve todos los alumnos como lista de dicts.
    Usado por el endpoint GET /alumnos.
    """
    return [a.to_dict() for a in Alumno.query.all()]


def get_alumno_by_id(alumno_id: int):
    """
    Devuelve un alumno por su ID.
    - Si existe → dict con los datos del alumno.
    - Si no existe → None.
    Usado por GET /alumnos/<id>.
    """
    alumno = Alumno.query.get(alumno_id)
    if alumno is None:
        return None
    return alumno.to_dict()


def create_alumno(data: dict):
    """
    Crea un alumno a partir de un dict `data` y devuelve sus datos como dict.

    La validación de duplicados por DNI la maneja la base de datos
    (constraint UNIQUE) y el endpoint captura IntegrityError para
    devolver 409 si corresponde.
    """
    alumno = Alumno(
        legajo=data.get("legajo"),
        nombre=data.get("nombre"),
        apellido=data.get("apellido"),
        dni=data.get("dni"),
        email=data.get("email"),
        facultad=data.get("facultad"),
        fecha_nacimiento=data.get("fecha_nacimiento"),
        carrera=data.get("carrera"),
        anio_ingreso=data.get("anio_ingreso"),
    )

    db.session.add(alumno)
    db.session.commit()

    return alumno.to_dict()

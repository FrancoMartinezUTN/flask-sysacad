from app.models.alumno import Alumno

def get_alumnos():
    return [alumno.to_dict() for alumno in Alumno.query.all()]

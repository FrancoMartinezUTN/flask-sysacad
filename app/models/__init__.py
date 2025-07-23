from .grado import Grado
from .facultad import Facultad
from .alumno import Alumno
from .materia import Materia
from .inscripcion import Inscripcion

def importar_modelos():
    return {
        'Grado': Grado,
        'Facultad': Facultad,
        'Alumno': Alumno,
        'Materia': Materia,
        'Inscripcion': Inscripcion
    }
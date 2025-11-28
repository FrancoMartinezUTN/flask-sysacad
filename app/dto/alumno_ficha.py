from dataclasses import dataclass, asdict
from typing import Optional
from app.models.alumno import Alumno

@dataclass
class AlumnoFicha:
    legajo: Optional[str]
    apellido: str
    nombre: str
    dni: str
    email: str
    facultad: Optional[str]

    def to_dict(self):
        return asdict(self)

def build_ficha_from_model(a: Alumno) -> AlumnoFicha:
    return AlumnoFicha(
        legajo=a.legajo,
        apellido=a.apellido,
        nombre=a.nombre,
        dni=a.dni,
        email=a.email,
        facultad=a.facultad or "N/D",
    )

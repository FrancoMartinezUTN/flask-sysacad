from typing import Optional
from app.models.alumno import Alumno

def get_by_id(alumno_id: int) -> Optional[Alumno]:
   
    return Alumno.query.get(alumno_id)

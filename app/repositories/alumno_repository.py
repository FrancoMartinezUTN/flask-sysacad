from __future__ import annotations

from typing import Any, Dict, Optional

from app.db import db
from app.models.alumno import Alumno


class AlumnoRepository:
    @staticmethod
    def get_by_id(alumno_id: int) -> Optional[Alumno]:
        # SQLAlchemy 2.x: usar Session.get()
        return db.session.get(Alumno, alumno_id)

    @staticmethod
    def paginate(page: int, per_page: int):
        # Flask-SQLAlchemy paginate (compatible con lo que ya venís usando)
        return Alumno.query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def create(data: Dict[str, Any]) -> Alumno:
        nuevo = Alumno(**data)
        db.session.add(nuevo)
        db.session.commit()
        return nuevo

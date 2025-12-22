# app/repositories/alumno_repository.py
from __future__ import annotations

from typing import Optional

from app import db
from app.models.alumno import Alumno


def get_by_id(alumno_id: int) -> Optional[Alumno]:
    """
    Devuelve Alumno por PK o None.

    SQLAlchemy 2.x: usar Session.get() en lugar de Alumno.query.get()
    (Query.get es legacy).
    """
    return db.session.get(Alumno, alumno_id)

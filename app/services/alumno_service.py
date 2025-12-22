from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from app.db import db
from app.models.alumno import Alumno
from app.repositories.alumno_repository import AlumnoRepository
from app.utils.cache import cache_get, cache_set, get_redis_connection

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# Conversión centralizada de Alumno -> dict
# -------------------------------------------------------------------
def _alumno_to_dict(alumno: Alumno) -> Dict[str, Any]:
    """
    Devuelve un dict con estructura estable para la API.
    Si el modelo implementa to_dict(), se usa eso.
    """
    if hasattr(alumno, "to_dict"):
        return alumno.to_dict()

    return {
        "id": alumno.id,
        "dni": alumno.dni,
        "nombre": alumno.nombre,
        "apellido": alumno.apellido,
        "email": getattr(alumno, "email", None),
        "facultad": getattr(alumno, "facultad", None),
        "carrera": getattr(alumno, "carrera", None),
        "anio_ingreso": getattr(alumno, "anio_ingreso", None),
    }


def _invalidar_cache_listas_alumnos() -> None:
    """
    Elimina todas las keys cacheadas de listados de alumnos.
    """
    r = get_redis_connection()
    if not r:
        return

    try:
        for key in r.scan_iter("alumnos_page_*"):
            r.delete(key)
    except Exception:
        logger.exception("Error limpiando caché de listas de alumnos")


# -------------------------------------------------------------------
# Servicios (la capa que deben usar las rutas)
# -------------------------------------------------------------------
def obtener_todos(page: int = 1, per_page: int = 20) -> Dict[str, Any]:
    """
    Retorna la lista de alumnos paginada.
    Usa Redis como caché si está disponible.
    """
    cache_key = f"alumnos_page_{page}_per_{per_page}"
    cached = cache_get(cache_key)
    if cached:
        logger.debug("Cache hit: %s", cache_key)
        return cached

    logger.debug("Cache miss: %s", cache_key)
    p = AlumnoRepository.paginate(page=page, per_page=per_page)

    data = {
        "items": [_alumno_to_dict(a) for a in p.items],
        "page": p.page,
        "pages": p.pages,
        "total": p.total,
        "per_page": p.per_page,
    }

    cache_set(cache_key, data, ttl=120)  # 2 minutos
    return data


def obtener_por_id(alumno_id: int) -> Optional[Dict[str, Any]]:
    """
    Retorna un alumno por ID como dict (API).
    """
    alumno = AlumnoRepository.get_by_id(alumno_id)
    if not alumno:
        return None
    return _alumno_to_dict(alumno)


def obtener_modelo_por_id(alumno_id: int) -> Optional[Alumno]:
    """
    Retorna el modelo ORM Alumno (para ficha/pdf/DTO).
    Las rutas NO deben usar repos directamente.
    """
    return AlumnoRepository.get_by_id(alumno_id)


def crear_alumno(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea un nuevo alumno y limpia la caché de listas de alumnos.
    Deja que IntegrityError suba (lo maneja la ruta con rollback).
    """
    nuevo = AlumnoRepository.create(data)
    _invalidar_cache_listas_alumnos()
    return _alumno_to_dict(nuevo)

from typing import Any, Dict, List, Optional

from app import db
from app.models.alumno import Alumno
from app.utils.cache import cache_get, cache_set, get_redis_connection
from app.repositories.alumno_repository import get_by_id  # ✅


def _alumno_to_dict(alumno: Alumno) -> Dict[str, Any]:
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


def obtener_todos(page: int = 1, per_page: int = 20) -> Dict[str, Any]:
    cache_key = f"alumnos_page_{page}_per_{per_page}"
    cached = cache_get(cache_key)

    if cached:
        print(f"✅ Cache hit: {cache_key}")
        return cached

    print(f"⚙️ Cache miss: {cache_key}")
    p = Alumno.query.paginate(page=page, per_page=per_page, error_out=False)

    data = {
        "items": [_alumno_to_dict(a) for a in p.items],
        "page": p.page,
        "pages": p.pages,
        "total": p.total,
        "per_page": p.per_page,
    }

    cache_set(cache_key, data, ttl=120)
    return data


def obtener_por_id(alumno_id: int) -> Optional[Dict[str, Any]]:
    alumno = get_by_id(alumno_id)  # ✅ repo (Session.get)
    if not alumno:
        return None
    return _alumno_to_dict(alumno)


def crear_alumno(data: Dict[str, Any]) -> Dict[str, Any]:
    nuevo = Alumno(**data)
    db.session.add(nuevo)
    db.session.commit()

    r = get_redis_connection()
    if r:
        try:
            for key in r.scan_iter("alumnos_page_*"):
                r.delete(key)
        except Exception as exc:
            print(f"⚠️ Error limpiando caché de alumnos: {exc}")

    return _alumno_to_dict(nuevo)

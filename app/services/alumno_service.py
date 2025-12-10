from typing import Any, Dict, List, Optional

from app import db
from app.models.alumno import Alumno
from app.utils.cache import cache_get, cache_set, get_redis_connection


# -------------------------------------------------------------------
# Conversión centralizada de Alumno -> dict
# -------------------------------------------------------------------
def _alumno_to_dict(alumno: Alumno) -> Dict[str, Any]:
    """
    Asegurate de que este dict respete la estructura que pide la cátedra.
    Si tu modelo Alumno tiene to_dict() y ya está bien definido, podés
    dejar simplemente `return alumno.to_dict()`.
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


# -------------------------------------------------------------------
# Servicios con soporte de caché Redis
# -------------------------------------------------------------------
def obtener_todos(page: int = 1, per_page: int = 20) -> Dict[str, Any]:
    """
    Retorna la lista de alumnos paginada.
    Estructura JSON:

    {
        "items": [...],
        "page": n,
        "pages": n,
        "total": n,
        "per_page": n
    }

    Usa Redis como caché si está disponible.
    """
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

    cache_set(cache_key, data, ttl=120)  # 2 minutos
    return data


def obtener_por_id(alumno_id: int) -> Optional[Dict[str, Any]]:
    """
    Retorna un alumno por ID (sin caché por simplicidad).
    """
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return None
    return _alumno_to_dict(alumno)


def crear_alumno(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea un nuevo alumno y limpia la caché de listas de alumnos.
    Lanza IntegrityError si viola UNIQUE (por ejemplo, DNI duplicado).
    """
    nuevo = Alumno(**data)
    db.session.add(nuevo)
    db.session.commit()

    # Invalidar TODAS las páginas cacheadas
    r = get_redis_connection()
    if r:
        try:
            for key in r.scan_iter("alumnos_page_*"):
                r.delete(key)
        except Exception as exc:
            print(f"⚠️ Error limpiando caché de alumnos: {exc}")

    return _alumno_to_dict(nuevo)

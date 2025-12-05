from typing import Optional

from app import db
from app.models.alumno import Alumno
from app.utils.cache import cache_get, cache_set, cache_delete_pattern


# -------------------------------------------------------------------
# Servicio de Alumnos con soporte de caché Redis
# -------------------------------------------------------------------


def _alumno_to_dict(alumno: Alumno) -> dict:
    """
    Punto único para convertir un Alumno a dict.
    Si mañana cambia la representación, se toca solo acá.
    """
    return alumno.to_dict()  # Ajustar si tu modelo usa otro método


def obtener_todos() -> list[dict]:
    """
    Retorna la lista de alumnos.
    - Primero intenta leer desde Redis.
    - Si no hay datos en cache, consulta la base y guarda el resultado.
    """
    cache_key = "alumnos:todos"
    cached = cache_get(cache_key)

    if cached is not None:
        print("✅ Cache hit: alumnos:todos (lista de alumnos desde Redis).")
        return cached

    print("⚙️ Cache miss: alumnos:todos – consultando base de datos.")
    alumnos = Alumno.query.all()
    data = [_alumno_to_dict(a) for a in alumnos]

    # TTL = 120 segundos (2 minutos)
    cache_set(cache_key, data, ttl_seconds=120)

    return data


def obtener_por_id(alumno_id: int) -> Optional[dict]:
    """
    Retorna un alumno por ID.
    - Usa cache por alumno individual: clave alumno:<id>.
    """
    cache_key = f"alumno:{alumno_id}"
    cached = cache_get(cache_key)

    if cached is not None:
        print(f"✅ Cache hit: {cache_key} (alumno desde Redis).")
        return cached

    print(f"⚙️ Cache miss: {cache_key} – consultando base de datos.")
    alumno = Alumno.query.get(alumno_id)
    if not alumno:
        return None

    data = _alumno_to_dict(alumno)

    # TTL un poco más largo para objetos individuales (5 minutos)
    cache_set(cache_key, data, ttl_seconds=300)

    return data


def create_alumno(data: dict) -> dict:
    """
    Crea un nuevo alumno y limpia la caché relacionada:
    - Lista de alumnos.
    - Cache puntual del alumno recién creado (por las dudas).
    """
    nuevo = Alumno(**data)
    db.session.add(nuevo)
    db.session.commit()

    data_dict = _alumno_to_dict(nuevo)

    # Invalidar cache relacionada
    # - lista global
    cache_delete_pattern("alumnos:todos")
    # - por si ya existía algo cacheado con ese id
    cache_delete_pattern(f"alumno:{nuevo.id}")

    return data_dict


# -------------------------------------------------------------------
# Aliases para compatibilidad con alumno_routes
# -------------------------------------------------------------------


def crear_alumno(data: dict) -> dict:
    """
    Alias de create_alumno para mantener compatibilidad con
    código existente que aún llame a crear_alumno().
    """
    return create_alumno(data)


def get_alumnos() -> list[dict]:
    """
    Alias en inglés para el listado de alumnos,
    usado por algunas rutas o capas superiores.
    """
    return obtener_todos()


def get_alumno_by_id(alumno_id: int) -> Optional[dict]:
    """
    Alias en inglés para obtener alumno por ID,
    usado por alumno_routes.
    """
    return obtener_por_id(alumno_id)

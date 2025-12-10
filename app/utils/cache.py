
import json
import os
from typing import Any, Optional

import redis

# Cache interno del cliente y flag para no insistir cuando Redis no está disponible
_redis_client: Optional[redis.Redis] = None
_redis_disabled: bool = False


def get_redis_connection() -> Optional[redis.Redis]:
    """
    Devuelve una conexión a Redis o None si no está disponible.

    Usa la variable de entorno REDIS_URL. Ejemplos:
    - redis://localhost:6379/0          (desarrollo local)
    - redis://redis-sysacad:6379/0      (docker-compose, servicio 'redis-sysacad')
    """
    global _redis_client, _redis_disabled

    if _redis_disabled:
        return None

    if _redis_client is not None:
        return _redis_client

    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    try:
        client = redis.from_url(redis_url, decode_responses=False)
        client.ping()
        print(f"✅ Redis conectado: {redis_url}")
        _redis_client = client
        return _redis_client
    except Exception as exc:
        # No hay Redis: se desactiva cache de forma segura
        print(f"⚠️ Redis no disponible, se desactiva caché. Detalle: {exc}")
        _redis_client = None
        _redis_disabled = True
        return None


def cache_get(key: str) -> Optional[Any]:
    """
    Lee un valor desde Redis (JSON serializado).
    Devuelve None si no hay cache o en caso de error.
    """
    client = get_redis_connection()
    if not client:
        return None

    try:
        raw = client.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    except Exception as exc:
        print(f"⚠️ Error leyendo caché [{key}]: {exc}")
        return None


def cache_set(key: str, value: Any, ttl: int = 60) -> None:
    """
    Guarda un valor en Redis serializado como JSON con TTL en segundos.
    Si Redis no está disponible, simplemente no hace nada.
    """
    client = get_redis_connection()
    if not client:
        return

    try:
        client.setex(key, ttl, json.dumps(value))
    except Exception as exc:
        print(f"⚠️ Error escribiendo caché [{key}]: {exc}")

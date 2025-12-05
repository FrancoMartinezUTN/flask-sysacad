import json
import logging
import os

import redis

_logger = logging.getLogger(__name__)
_redis_client = None


def _get_redis_client():
    """
    Devuelve un cliente Redis singleton.
    Si no se puede conectar, devuelve None y la cache queda deshabilitada
    sin romper la app.
    """
    global _redis_client

    if _redis_client is not None:
        return _redis_client

    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

    try:
        client = redis.Redis.from_url(redis_url, decode_responses=True)
        # Verificación rápida de conexión
        client.ping()
        _logger.info("Conectado a Redis en %s", redis_url)
        _redis_client = client
    except Exception as exc:  # noqa: BLE001
        _logger.warning(
            "No se pudo conectar a Redis (%s). La cache queda deshabilitada.",
            exc,
        )
        _redis_client = None

    return _redis_client


def cache_get(key: str):
    """
    Obtiene un valor JSON desde Redis.
    Devuelve el objeto Python o None si no existe / falla.
    """
    client = _get_redis_client()
    if not client:
        return None

    try:
        raw = client.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    except Exception:  # noqa: BLE001
        _logger.exception("Error leyendo clave '%s' desde Redis", key)
        return None


def cache_set(key: str, value, ttl_seconds: int = 60):
    """
    Guarda un objeto Python como JSON en Redis con un TTL (segundos).
    Si Redis no está disponible, no rompe la app.
    """
    client = _get_redis_client()
    if not client:
        return

    try:
        payload = json.dumps(value)
        client.setex(key, ttl_seconds, payload)
    except Exception:  # noqa: BLE001
        _logger.exception("Error guardando clave '%s' en Redis", key)


def cache_delete_pattern(pattern: str):
    """
    Borra todas las claves que matcheen un patrón, por ejemplo:
    'alumno:123' o 'alumno:*'
    """
    client = _get_redis_client()
    if not client:
        return

    try:
        for key in client.scan_iter(match=pattern):
            client.delete(key)
    except Exception:  # noqa: BLE001
        _logger.exception("Error borrando claves por patrón '%s' en Redis", pattern)

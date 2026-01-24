#!/usr/bin/env python
"""
Init de DB para Docker (one-shot job).
- Espera a que la app pueda conectar a Postgres.
- Importa modelos para registrar metadata.
- Ejecuta migrations (Alembic) o fallback a create_all().
"""

import os
import sys
import time
import traceback
import importlib
import pkgutil
from pathlib import Path

MAX_RETRIES = int(os.getenv("DB_INIT_MAX_RETRIES", "30"))
RETRY_DELAY = float(os.getenv("DB_INIT_RETRY_DELAY", "2"))


def _import_all_models():
    """
    Importa todos los módulos dentro de app.models (si existe)
    para registrar las tablas en metadata antes de create_all().
    """
    try:
        models_pkg = importlib.import_module("app.models")
    except Exception:
        return

    if not hasattr(models_pkg, "__path__"):
        return

    for mod in pkgutil.iter_modules(models_pkg.__path__):
        name = mod.name
        try:
            importlib.import_module(f"app.models.{name}")
        except Exception:
            print(f"[WARN] No se pudo importar app.models.{name}", file=sys.stderr)


def _run_migrations(app):
    """
    Intenta ejecutar migraciones Alembic si existe el directorio migrations/.
    Retorna True si se ejecutaron, False si no hay migraciones.
    """
    migrations_dir = Path(app.root_path).parent / "migrations"
    if not migrations_dir.exists():
        return False

    try:
        from flask_migrate import upgrade
        with app.app_context():
            upgrade()
        return True
    except Exception as e:
        print(f"[WARN] Error ejecutando migraciones: {e}", file=sys.stderr)
        return False


def main() -> int:
    last_err = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            from app import create_app
            from app.db import db

            app = create_app()

            with app.app_context():
                _import_all_models()

                # Intentar migraciones primero, fallback a create_all
                if _run_migrations(app):
                    print("✅ DB inicializada via Alembic migrations")
                else:
                    db.create_all()
                    print("✅ DB inicializada via create_all() (sin migraciones)")

            return 0

        except Exception as e:
            last_err = e
            print(f"⏳ Init DB falló (intento {attempt}/{MAX_RETRIES}): {e}", file=sys.stderr)
            traceback.print_exc()

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

    print("❌ No se pudo inicializar la DB luego de reintentos.", file=sys.stderr)
    if last_err:
        print(f"Último error: {last_err}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

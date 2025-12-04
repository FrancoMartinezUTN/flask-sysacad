import os
import pytest

from app import create_app, db
from app.models.alumno import Alumno


@pytest.fixture
def client():
    """
    Crea una app Flask en modo testing, con BD en memoria,
    carga un alumno de ejemplo y expone un test_client.
    """

    # Configuración mínima para que la app arranque
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    os.environ["FLASK_CONTEXT"] = "testing"
    os.environ["FLASK_SKIP_DOTENV"] = "1"  # no leer .env en tests

    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

        # Alumno de prueba (campos basados en la API actual de /alumnos)
        alumno = Alumno(
            dni="40123456",
            nombre="Ana",
            apellido="Pérez",
            email="ana@example.com",
            facultad="FRC - UTN",
            legajo="2025-0001",
        )
        db.session.add(alumno)
        db.session.commit()
        alumno_id = alumno.id

    # Creamos el cliente de pruebas y le colgamos el id del alumno de prueba
    with app.test_client() as testing_client:
        testing_client.alumno_id = alumno_id
        yield testing_client

    # Limpieza de variables de entorno
    for var in ("SECRET_KEY", "SQLALCHEMY_DATABASE_URI", "FLASK_CONTEXT", "FLASK_SKIP_DOTENV"):
        os.environ.pop(var, None)


def test_get_alumnos_ok(client):
    """
    GET /alumnos debe responder 200 y devolver un JSON
    con la clave 'items' y al menos un alumno.
    """
    resp = client.get("/alumnos")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, dict)
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 1


def test_get_alumno_por_id_ok(client):
    """
    GET /alumnos/<id> con un id existente debe responder 200
    y devolver los datos del alumno de prueba.
    """
    alumno_id = client.alumno_id
    resp = client.get(f"/alumnos/{alumno_id}")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["dni"] == "40123456"
    assert data["nombre"] == "Ana"
    assert data["apellido"] == "Pérez"


def test_get_alumno_por_id_not_found(client):
    """
    GET /alumnos/<id> con un id inexistente debe responder 404.
    """
    resp = client.get("/alumnos/999999")
    assert resp.status_code == 404


def test_post_alumno_crea_ok(client):
    """
    POST /alumnos con datos válidos debe crear un alumno
    y responder 201 (o 200 según implementación actual).
    """
    nuevo = {
        "dni": "40123457",
        "nombre": "Juan",
        "apellido": "García",
        "email": "juan@example.com",
        "facultad": "FRC - UTN",
        "legajo": "2025-0002",
    }

    resp = client.post("/alumnos", json=nuevo)
    assert resp.status_code in (200, 201)


def test_post_alumno_dni_duplicado(client):
    """
    POST /alumnos con un DNI ya existente debe responder 409 (conflicto).
    """
    duplicado = {
        "dni": "40123456",  # mismo que el alumno cargado en el fixture
        "nombre": "Ana Duplicada",
        "apellido": "Pérez",
        "email": "ana.dup@example.com",
        "facultad": "FRC - UTN",
        "legajo": "2025-9999",
    }

    resp = client.post("/alumnos", json=duplicado)
    assert resp.status_code == 409

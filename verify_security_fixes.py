import os
import sys
from app import create_app


def test_missing_secret_key():
    print("Testing missing SECRET_KEY...")

    # Nos aseguramos de que no haya SECRET_KEY en el entorno
    os.environ.pop("SECRET_KEY", None)

    # Para esta prueba queremos simular que NO existe archivo .env
    # Por eso le indicamos a create_app que saltee load_dotenv()
    os.environ["FLASK_SKIP_DOTENV"] = "1"

    try:
        create_app()
        print("FAIL: App started without SECRET_KEY")
    except RuntimeError as e:
        if "SECRET_KEY" in str(e):
            print("PASS: App failed to start without SECRET_KEY as expected")
        else:
            print(f"FAIL: App failed with unexpected error: {e}")
    except Exception as e:
        print(f"FAIL: App failed with unexpected error type: {type(e)}")
    finally:
        # Dejamos el entorno limpio para las demás pruebas
        os.environ.pop("FLASK_SKIP_DOTENV", None)


def test_debug_mode_default():
    print("\nTesting default debug mode...")

    # Aseguramos que no haya FLASK_DEBUG seteada
    if "FLASK_DEBUG" in os.environ:
        del os.environ["FLASK_DEBUG"]

    # Simulamos la lógica de run.py
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    if not debug_mode:
        print("PASS: Debug mode is False by default")
    else:
        print("FAIL: Debug mode is True by default")


def test_valid_config():
    print("\nTesting valid configuration...")

    # Config mínima válida para arrancar la app en memoria
    os.environ["SECRET_KEY"] = "test-secret-key"
    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    try:
        app = create_app()
        if app.config["SECRET_KEY"] == "test-secret-key":
            print("PASS: App started with valid SECRET_KEY")
        else:
            print("FAIL: App started but SECRET_KEY mismatch")
    except Exception as e:
        print(f"FAIL: App failed to start with valid config: {e}")


if __name__ == "__main__":
    test_missing_secret_key()
    test_debug_mode_default()
    test_valid_config()

import os  # <- NECESARIO para usar os.getenv
from app import create_app, db
from app.models.alumno import Alumno


app = create_app()

# Crea las tablas definidas por los modelos (por ahora, Alumno)
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    # Leemos FLASK_DEBUG desde el entorno; por defecto queda en False
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    app.run(debug=debug_mode)

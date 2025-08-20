from app import create_app
from app.db import db

app = create_app()

with app.app_context():
    print("🚧 Creando tablas en la base de datos...")
    db.create_all()
    print("✅ Tablas creadas exitosamente.")


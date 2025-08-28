from app import create_app
from app.db import db

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Tablas creadas/actualizadas.")

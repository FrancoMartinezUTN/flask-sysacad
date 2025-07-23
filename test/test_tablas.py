from app import create_app, db

def test_tablas_existentes():
    app = create_app()
    with app.app_context():
        db.create_all()
        tablas = db.metadata.tables.keys()
        print(f"TABLAS EN LA DB: {list(tablas)}")
        assert "facultades" in tablas
        assert "grado" in tablas  # Según __tablename__ en grado.py
        assert "alumnos" in tablas
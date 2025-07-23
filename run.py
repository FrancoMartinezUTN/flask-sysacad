from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()  # Crear tablas en contexto seguro

if __name__ == '__main__':
    app.run(debug=True)
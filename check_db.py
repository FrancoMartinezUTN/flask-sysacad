from app import create_app
app = create_app()
with app.app_context():
    from app.models import Grado
    grados = Grado.query.all()
    for grado in grados:
        print(f"ID: {grado.id}, Nombre: {grado.nombre}")
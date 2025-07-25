from app import create_app
app = create_app()
with app.app_context():
    from app.models import Grado, Materia
    print("Grados:", Grado.query.all())
    print("Materias:", Materia.query.all())
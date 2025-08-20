import textwrap
from app.models import Alumno
from app.db import db

def test_importar_alumnos_inserta_y_no_duplica(runner, app):
    csv_data = textwrap.dedent("""\
        dni,nombre,apellido,email
        123,Juan,Pérez,juan@example.com
        456,Ana,López,ana@example.com
    """)
    # Guardamos CSV temporal
    with open("alumnos_test.csv", "w", encoding="utf-8") as f:
        f.write(csv_data)

    # Inserción inicial
    r1 = runner.invoke(args=["importar", "alumnos", "alumnos_test.csv"])
    assert r1.exit_code == 0

    # Reintento (no debe duplicar)
    r2 = runner.invoke(args=["importar", "alumnos", "alumnos_test.csv"])
    assert r2.exit_code == 0

    # Verificación en la DB real
    assert db.session.query(Alumno).filter_by(dni=123).count() == 1
    assert db.session.query(Alumno).filter_by(dni=456).count() == 1
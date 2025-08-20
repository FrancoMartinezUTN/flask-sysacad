from pathlib import Path
from app.models import Facultad, Grado, Materia
from app.db import db

def test_importar_xml_grados_facultades_materias(runner, app, tmp_path):
    xml = tmp_path / "datos.xml"
    xml.write_text("""<?xml version="1.0" encoding="UTF-8"?>
    <root>
      <facultades>
        <facultad codigo="F1" nombre="Facu Test"/>
      </facultades>
      <grados>
        <grado codigo="G1" nombre="Grado Test"/>
      </grados>
      <materias>
        <materia codigo="M1" nombre="Materia Test"/>
      </materias>
    </root>
    """, encoding="utf-8")

    r = runner.invoke(args=["importar", "xml", str(xml)])
    assert r.exit_code == 0

    # Verificación en la DB real
    assert db.session.query(Facultad).filter_by(codigo="F1").count() == 1
    assert db.session.query(Grado).filter_by(codigo="G1").count() == 1
    assert db.session.query(Materia).filter_by(codigo="M1").count() == 1
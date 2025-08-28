import pandas as pd
from app import create_app
from app.db import db
from app.models.alumno import Alumno

def importar_alumnos(csv_path: str):
    app = create_app()
    with app.app_context():
        df = pd.read_csv(csv_path, dtype=str).fillna("")

        # DNIs existentes para evitar duplicados
        existentes = {dni for (dni,) in db.session.query(Alumno.dni).all()}

        nuevos = []
        for _, row in df.iterrows():
            dni = row.get("dni", "").strip()
            if not dni or dni in existentes:
                continue

            email = (row.get("email") or f"{row.get('nombre','').strip()}.{row.get('apellido','').strip()}@utn.edu").lower()

            a = Alumno(
                nombre=row.get("nombre","").strip(),
                apellido=row.get("apellido","").strip(),
                dni=dni,
                email=email,
                # si tenés estos campos en el CSV, mapéalos:
                # fecha_nacimiento=pd.to_datetime(row.get("fecha_nacimiento"), errors="coerce"),
                carrera=row.get("carrera","").strip(),
                anio_ingreso=int(row["anio_ingreso"]) if str(row.get("anio_ingreso","")).isdigit() else None,
            )
            nuevos.append(a)

        if nuevos:
            db.session.bulk_save_objects(nuevos)
            db.session.commit()
            print(f"Importados {len(nuevos)} alumnos nuevos.")
        else:
            print("No hay alumnos nuevos para importar.")

if __name__ == "__main__":
    # ejemplo: python -m app.importers.importar_alumnos alumnos.csv
    importar_alumnos("alumnos.csv")

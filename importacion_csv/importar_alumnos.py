import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.alumno import Alumno

def importar_alumnos_csv(path_csv: str):
    try:
        print("🚀 Iniciando importación...")

        df = pd.read_csv(path_csv)

        session: Session = SessionLocal()

        # Asegurar que todos los DNI se comparen como string
        dnis_existentes = set(str(dni) for (dni,) in session.query(Alumno.dni).all())

        alumnos = []
        nuevos = 0

        for _, row in df.iterrows():
            dni = str(row['nro_documento'])

            if dni not in dnis_existentes:
                alumno = Alumno(
                    nombre=row['nombre'],
                    apellido=row['apellido'],
                    dni=dni,
                    email=f"{row['nombre'].lower()}.{row['apellido'].lower()}@mail.com",
                    fecha_nacimiento=row['fecha_nacimiento'],
                    carrera="Ingeniería en Sistemas",
                    año_ingreso=int(str(row['fecha_ingreso'])[:4])
                )
                alumnos.append(alumno)
                dnis_existentes.add(dni)  # para evitar duplicados dentro del mismo CSV
                nuevos += 1

        print(f"✅ Se importarán {nuevos} alumnos nuevos (sin duplicados).")

        if alumnos:
            session.bulk_save_objects(alumnos)
            session.commit()

        session.close()

        print("✅ Importación finalizada y guardada en la base de datos.")

    except Exception as e:
        print("❌ Ocurrió un error durante la importación:")
        print(e)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("❌ Debe indicar la ruta del archivo CSV como argumento.")
    else:
        importar_alumnos_csv(sys.argv[1])

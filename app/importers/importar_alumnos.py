import pandas as pd
import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.alumno import Alumno

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def importar_alumnos_csv(path_csv: str):
    """Importa alumnos desde un archivo CSV a la base de datos."""
    session: Session = None
    try:
        logging.info("🚀 Iniciando importación desde %s...", path_csv)

        # Leer archivo CSV
        df = pd.read_csv(path_csv)

        # Abrir sesión con la base de datos
        session = SessionLocal()

        # Leer DNIs ya existentes desde la base
        dnis_existentes = set(str(dni) for (dni,) in session.query(Alumno.dni).all())

        alumnos_nuevos = []
        nuevos = 0

        # Procesar cada fila
        for _, row in df.iterrows():
            dni = str(row['nro_documento'])

            if dni not in dnis_existentes:
                # Limpiar nombre y apellido para email
                nombre_clean = row['nombre'].lower().replace(" ", "")
                apellido_clean = row['apellido'].lower().replace(" ", "")
                email_generado = f"{nombre_clean}.{apellido_clean}.{dni}@mail.com"

                alumno = Alumno(
                    nombre=row['nombre'],
                    apellido=row['apellido'],
                    dni=dni,
                    email=email_generado,
                    fecha_nacimiento=row['fecha_nacimiento'],
                    carrera="Ingeniería en Sistemas",
                    año_ingreso=int(str(row['fecha_ingreso'])[:4])
                )
                alumnos_nuevos.append(alumno)
                dnis_existentes.add(dni)
                nuevos += 1

        logging.info("✅ Se importarán %d alumnos nuevos (sin duplicados).", nuevos)

        if alumnos_nuevos:
            session.bulk_save_objects(alumnos_nuevos)
            session.commit()
            logging.info("✅ Importación finalizada y guardada en la base de datos.")
        else:
            logging.warning("⚠️ No hay alumnos nuevos para importar.")

    except Exception as e:
        logging.error("❌ Error durante la importación: %s", e)
        if session:
            session.rollback()
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        logging.error("Debe indicar la ruta del archivo CSV como argumento.")
    else:
        importar_alumnos_csv(sys.argv[1])

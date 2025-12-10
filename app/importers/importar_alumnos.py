import csv
import sys
from datetime import datetime
from pathlib import Path

from sqlalchemy.exc import IntegrityError

from app import create_app, db
from app.models.alumno import Alumno

# --------------------------------------------------------------------
# Setup de la app para usar la misma config que el resto del proyecto
# --------------------------------------------------------------------
app = create_app()
app.app_context().push()


def _parse_fecha(fecha_str: str):
    """
    Convierte un string de fecha en date, tolerando varios formatos.
    Si no puede parsear, devuelve None.
    """
    if not fecha_str:
        return None

    s = str(fecha_str).strip()
    if not s:
        return None

    formatos = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d")
    for fmt in formatos:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def importar_desde_csv(csv_path: str) -> None:
    """
    Importa alumnos desde un CSV.
    - Mapea:
        nro_documento -> dni
        nro_legajo    -> legajo
        fecha_ingreso -> anio_ingreso (sólo año)
    - Evita:
        * duplicados ya existentes en la DB (por dni)
        * duplicados dentro del propio CSV (por dni)
    """
    path = Path(csv_path)

    if not path.is_file():
        print(f"❌ No se encontró el archivo CSV: {path}")
        return

    print(f"📥 Leyendo CSV: {path.name}")

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        print(f"🧾 Campos detectados en el CSV: {fieldnames}")

        # ------------------------------
        # 1) Traer DNIs ya existentes
        # ------------------------------
        existing_dnis = {
            dni for (dni,) in db.session.query(Alumno.dni).all() if dni is not None
        }
        print(f"📊 Alumnos existentes en DB: {len(existing_dnis)}")

        dni_vistos = set(existing_dnis)

        nuevos: list[Alumno] = []
        total_filas = 0
        duplicados_csv = 0
        sin_dni = 0

        # ------------------------------
        # 2) Recorrer filas del CSV
        # ------------------------------
        for row in reader:
            total_filas += 1

            dni = (row.get("nro_documento") or "").strip()
            if not dni:
                sin_dni += 1
                continue

            # Si el DNI ya está en DB o ya apareció en este mismo CSV => se descarta
            if dni in dni_vistos:
                duplicados_csv += 1
                continue
            dni_vistos.add(dni)

            legajo = (row.get("nro_legajo") or "").strip()
            nombre = (row.get("nombre") or "").strip()
            apellido = (row.get("apellido") or "").strip()

            fecha_nac = _parse_fecha(row.get("fecha_nacimiento") or "")

            # Año de ingreso a partir de fecha_ingreso
            fecha_ing = (row.get("fecha_ingreso") or "").strip()
            anio_ingreso = None
            if fecha_ing:
                fecha_ing_parsed = _parse_fecha(fecha_ing)
                if fecha_ing_parsed:
                    anio_ingreso = fecha_ing_parsed.year
                else:
                    try:
                        anio_ingreso = int(str(fecha_ing)[:4])
                    except ValueError:
                        anio_ingreso = None

            alumno = Alumno(
                legajo=legajo,
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                fecha_nacimiento=fecha_nac,
                anio_ingreso=anio_ingreso,
            )
            nuevos.append(alumno)

    print(f"➡️ Filas leídas (sin header): {total_filas}")
    print(f"🔁 DNI duplicados (CSV + DB): {duplicados_csv}")
    print(f"🚫 Filas sin DNI: {sin_dni}")
    print(f"🆕 Alumnos nuevos a insertar (limpios): {len(nuevos)}")

    if not nuevos:
        print("✅ No hay alumnos nuevos para importar.")
        return

    # ------------------------------
    # 3) Inserción en bloque
    # ------------------------------
    try:
        db.session.bulk_save_objects(nuevos)
        db.session.commit()
        print(f"✅ Importación finalizada. Alumnos insertados: {len(nuevos)}")
    except IntegrityError as e:
        db.session.rollback()
        print("❌ Error de integridad al insertar en DB (posible DNI duplicado remanente).")
        print(str(e))


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python -m app.importers.importar_alumnos <ruta_csv>")
        sys.exit(1)

    importar_desde_csv(sys.argv[1])


if __name__ == "__main__":
    main()

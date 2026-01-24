from io import BytesIO

from flask import Blueprint, abort, jsonify, request, send_file
from sqlalchemy.exc import IntegrityError

from app.db import db
from app.dto.alumno_ficha import build_ficha_from_model
from app.renderers.pdf.alumno_pdf_renderer import render_alumno_ficha_pdf
from app.services.alumno_service import (
    crear_alumno,
    obtener_modelo_por_id,
    obtener_por_id,
    obtener_todos,
)

alumno_bp = Blueprint("alumno_bp", __name__)

# límites para paginación (evita abuso)
MAX_PER_PAGE = 100


def _parse_int_arg(name: str, default: int, min_value: int, max_value: int) -> int:
    """
    Parseo/validación centralizada de query params enteros.
    """
    raw = request.args.get(name, default)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        abort(400, description=f"Parámetro '{name}' inválido. Debe ser entero.")

    if value < min_value or value > max_value:
        abort(
            400,
            description=f"Parámetro '{name}' fuera de rango ({min_value}-{max_value}).",
        )
    return value


@alumno_bp.route("/alumnos", methods=["GET"])
def listar_alumnos():
    page = _parse_int_arg("page", default=1, min_value=1, max_value=10_000)
    per_page = _parse_int_arg("per_page", default=20, min_value=1, max_value=MAX_PER_PAGE)

    data = obtener_todos(page=page, per_page=per_page)
    return jsonify(data), 200


@alumno_bp.route("/alumnos", methods=["POST"])
def crear_alumno_route():
    payload = request.get_json(silent=True) or {}

    if not isinstance(payload, dict) or not payload:
        return jsonify({"error": "Body JSON inválido o vacío"}), 400

    try:
        alumno_dict = crear_alumno(payload)
        return jsonify(alumno_dict), 201
    except IntegrityError:
        # importante: limpiar sesión tras violación de UNIQUE
        db.session.rollback()
        return jsonify({"error": "Ya existe un alumno con ese DNI"}), 409


@alumno_bp.route("/alumnos/<int:alumno_id>", methods=["GET"])
def obtener_alumno_por_id_route(alumno_id: int):
    alumno = obtener_por_id(alumno_id)
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return jsonify(alumno), 200


@alumno_bp.route("/alumnos/<int:alumno_id>/ficha.json", methods=["GET"])
def alumno_ficha_json(alumno_id: int):
    """
    Ficha del alumno en JSON (sin repo en la ruta).
    """
    a = obtener_modelo_por_id(alumno_id)
    if not a:
        abort(404, description="Alumno no encontrado")

    ficha = build_ficha_from_model(a)
    return jsonify(ficha.to_dict()), 200


@alumno_bp.route("/alumnos/<int:alumno_id>/ficha.pdf", methods=["GET"])
def alumno_ficha_pdf(alumno_id: int):
    """
    Ficha del alumno en PDF (sin repo en la ruta).
    """
    a = obtener_modelo_por_id(alumno_id)
    if not a:
        abort(404, description="Alumno no encontrado")

    ficha = build_ficha_from_model(a)
    pdf_bytes = render_alumno_ficha_pdf(ficha)

    return send_file(
        BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=False,
        download_name=f"ficha_alumno_{alumno_id}.pdf",
    )

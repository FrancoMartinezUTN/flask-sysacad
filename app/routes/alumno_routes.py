from flask import Blueprint, jsonify, request, abort, send_file
from io import BytesIO
from sqlalchemy.exc import IntegrityError

from app.db import db
from app.services.alumno_service import (
    obtener_todos,
    obtener_por_id,
    crear_alumno,
)
from app.repositories.alumno_repo import get_by_id
from app.dto.alumno_ficha import build_ficha_from_model
from app.renderers.pdf.alumno_pdf_renderer import render_alumno_ficha_pdf

alumno_bp = Blueprint("alumno_bp", __name__)


@alumno_bp.route("/alumnos", methods=["GET"])
def listar_alumnos():
    """
    Lista de alumnos paginada.

    Estructura JSON de respuesta:

    {
        "items": [...],
        "page": n,
        "pages": n,
        "total": n,
        "per_page": n
    }

    Los datos se obtienen a través del servicio, que puede usar caché Redis.
    """
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 20))

    data = obtener_todos(page=page, per_page=per_page)
    return jsonify(data), 200


@alumno_bp.route("/alumnos", methods=["POST"])
def crear_alumno_route():
    """
    Crea un alumno.
    - 201 si se crea correctamente.
    - 409 si el DNI ya existe (conflicto, UNIQUE en la BD).
    """
    payload = request.get_json() or {}

    try:
        alumno_dict = crear_alumno(payload)
        return jsonify(alumno_dict), 201
    except IntegrityError:
        # MUY IMPORTANTE: limpiar la sesión luego de la violación de UNIQUE
        db.session.rollback()
        return jsonify({"error": "Ya existe un alumno con ese DNI"}), 409


@alumno_bp.route("/alumnos/<int:alumno_id>", methods=["GET"])
def obtener_alumno_por_id_route(alumno_id: int):
    """
    Devuelve un alumno por su ID.
    - 200 si existe.
    - 404 si no existe.
    """
    alumno = obtener_por_id(alumno_id)

    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404

    return jsonify(alumno), 200


@alumno_bp.route("/alumnos/<int:alumno_id>/ficha.json", methods=["GET"])
def alumno_ficha_json(alumno_id: int):
    """
    Ficha del alumno en JSON (usa el repositorio y DTO existentes).
    """
    a = get_by_id(alumno_id)
    if not a:
        abort(404, description="Alumno no encontrado")
    ficha = build_ficha_from_model(a)
    return jsonify(ficha.to_dict())


@alumno_bp.route("/alumnos/<int:alumno_id>/ficha.pdf", methods=["GET"])
def alumno_ficha_pdf(alumno_id: int):
    """
    Ficha del alumno en PDF.
    """
    a = get_by_id(alumno_id)
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

from flask import Blueprint, jsonify, request, abort, send_file
from io import BytesIO

from app.models.alumno import Alumno
from app.services.alumno_service import create_alumno
from app.repositories.alumno_repo import get_by_id
from app.dto.alumno_ficha import build_ficha_from_model
from app.renderers.pdf.alumno_pdf_renderer import render_alumno_ficha_pdf

alumno_bp = Blueprint('alumno_bp', __name__)

@alumno_bp.route('/alumnos', methods=['GET'])
def listar_alumnos():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    p = Alumno.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "items": [a.to_dict() for a in p.items],
        "page": p.page,
        "pages": p.pages,
        "total": p.total,
        "per_page": p.per_page
    })

@alumno_bp.route('/alumnos', methods=['POST'])
def crear_alumno_route():
    data = request.get_json(force=True)
    return jsonify(create_alumno(data)), 201

@alumno_bp.route('/alumnos/<int:alumno_id>/ficha.json', methods=['GET'])
def alumno_ficha_json(alumno_id: int):
    a = get_by_id(alumno_id)
    if not a:
        abort(404, description="Alumno no encontrado")
    ficha = build_ficha_from_model(a)
    return jsonify(ficha.to_dict())

@alumno_bp.route('/alumnos/<int:alumno_id>/ficha.pdf', methods=['GET'])
def alumno_ficha_pdf(alumno_id: int):
    a = get_by_id(alumno_id)
    if not a:
        abort(404, description="Alumno no encontrado")
    ficha = build_ficha_from_model(a)
    pdf_bytes = render_alumno_ficha_pdf(ficha)
    return send_file(
        BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=False,
        download_name=f"ficha_alumno_{alumno_id}.pdf"
    )

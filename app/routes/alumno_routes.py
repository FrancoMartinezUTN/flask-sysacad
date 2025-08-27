from flask import Blueprint, jsonify, request
from app.services.alumno_service import get_alumnos, create_alumno

alumno_bp = Blueprint('alumno_bp', __name__)

@alumno_bp.route('/alumnos', methods=['GET'])
def listar_alumnos():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    from app.models.alumno import Alumno
    p = Alumno.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "items": [a.to_dict() for a in p.items],
        "page": p.page, "pages": p.pages, "total": p.total, "per_page": p.per_page
    })

@alumno_bp.route('/alumnos', methods=['POST'])
def crear_alumno():
    data = request.get_json(force=True)  # fuerza JSON si viene con content-type correcto
    creado = create_alumno(data)
    return jsonify(creado), 201

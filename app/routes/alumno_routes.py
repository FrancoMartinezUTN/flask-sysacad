from flask import Blueprint, jsonify
from app.services.alumno_service import get_alumnos

alumno_bp = Blueprint('alumno_bp', __name__)

@alumno_bp.route('/alumnos')
def listar_alumnos():
    return jsonify(get_alumnos())

from flask import Blueprint, request, jsonify
from app.services.materia_service import obtener_materias, crear_materia

materia_bp = Blueprint('materia_bp', __name__)

@materia_bp.route('/materias', methods=['GET'])
def get_materias():
    return jsonify(obtener_materias())

@materia_bp.route('/materias', methods=['POST'])
def post_materia():
    data = request.get_json()
    return jsonify(crear_materia(data)), 201

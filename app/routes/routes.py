from flask import Blueprint, jsonify, abort, render_template
from app.models import Grado, Materia

main_bp = Blueprint('main', __name__)

@main_bp.route('/grados', methods=['GET'])
def get_grados():
    grados = Grado.query.all()
    return jsonify([{"id": grado.id, "nombre": grado.nombre} for grado in grados])

@main_bp.route('/grados/<int:id>', methods=['GET'])
def get_grado(id):
    grado = Grado.query.get_or_404(id)
    return jsonify({"id": grado.id, "nombre": grado.nombre})

@main_bp.route('/materias', methods=['GET'])
def get_materias():
    materias = Materia.query.all()
    return jsonify([{"id": materia.id, "nombre": materia.nombre, "grado_id": materia.grado_id} for materia in materias])

@main_bp.route('/', methods=['GET'])
def index():
    grados = Grado.query.all()
    materias = Materia.query.all()
    return render_template('grados.html', grados=grados, materias=materias)
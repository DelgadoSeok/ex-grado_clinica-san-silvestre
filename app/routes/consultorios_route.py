from flask import Blueprint, render_template, request, jsonify
from services.consultorios_service import obtener_consultorios, registrar_consultorio
from datetime import datetime

consultorios_bp = Blueprint('consultorios', __name__, url_prefix='/consultorios')

@consultorios_bp.route('/', methods=['GET'])
def consultorios():
    consultorios = obtener_consultorios()
    return render_template('views/consultorios.html', consultorios=consultorios)

@consultorios_bp.route('/registrar', methods=['POST'])
def consultorios_dos():
    data = request.json
    print(data)
    resultado = registrar_consultorio(data)
    return jsonify(resultado)
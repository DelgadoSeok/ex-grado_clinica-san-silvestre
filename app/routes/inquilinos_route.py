from flask import Blueprint, render_template, request, jsonify
from services.inquilinos_service import registrar_inquilino, obtener_inquilinos, descartar_inquilino, editar_inquilino

inquilinos_bp = Blueprint('inquilinos', __name__, url_prefix='/inquilinos')

@inquilinos_bp.route('views//inquilinos')
def contratos():
    return render_template('views/inquilinos.html')

@inquilinos_bp.route('/', methods=['GET'])
def mostrar_inquilinos():
    inquilinos = obtener_inquilinos()
    return render_template('views/inquilinos.html', inquilinos=inquilinos)

@inquilinos_bp.route('/registrar', methods=['POST'])
def registrar_nuevo_inquilino():
    """ API para registrar un inquilino """
    data = request.json

    nombres = data.get("nombres")
    apellidos = data.get("apellidos")
    ci = data.get("ci")
    telf = data.get("telf")
    direccion = data.get("direccion")

    if not (nombres and apellidos and ci):
        return jsonify({"success": False, "error": "Datos incompletos"}), 400

    resultado = registrar_inquilino(nombres, apellidos, ci, telf, direccion)
    return jsonify(resultado)


@inquilinos_bp.route('/descartar/<int:id>', methods=['POST'])
def descartar(id):
    resultado = descartar_inquilino(id)
    return jsonify(resultado)

@inquilinos_bp.route('/editar/<int:id>', methods=['POST'])
def actualizar_inquilino(id):
    """ API para editar un inquilino """
    data = request.json
    nombres = data.get("nombres")
    apellidos = data.get("apellidos")
    ci = data.get("ci")
    telf = data.get("telf")
    direccion = data.get("direccion")

    resultado = editar_inquilino(id, nombres, apellidos, ci, telf, direccion)
    return jsonify(resultado)

@inquilinos_bp.route('/inquilinos')
def inquilinos():
    return render_template('views/inquilinos.html')

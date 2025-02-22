from flask import Blueprint, render_template, request, jsonify
from services.egresos_service import ver_egresos, crear_egreso, ver_tipos_egreso, editar_egreso

egresos_secre_bp = Blueprint('egresos_secre', __name__, url_prefix='/egresos_secre')

@egresos_secre_bp.route('/egresos_secre')
def contratos():
    return render_template('egresos_secre.html')

@egresos_secre_bp.route('/', methods=['GET'])
def mostrar_egresos():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    egresos = ver_egresos(fecha_inicio or None, fecha_fin or None)
    print("ver_egresos", egresos)
    return render_template('egresos_secre.html', egresos=egresos)

@egresos_secre_bp.route('/registrar', methods=['POST'])
def nuevo_egreso():
    data = request.json
    print("verdata", data)
    observacion = data.get('observacion')
    monto = data.get('monto')
    fecha = data.get('fecha')
    egreso_tipo_id = data.get('egreso_tipo_id')

    if not (observacion and monto and fecha and egreso_tipo_id):
        return jsonify({'error': 'Faltan datos'}), 400

    resultado = crear_egreso(observacion, monto, fecha, egreso_tipo_id)

    if resultado["success"]:
        return jsonify({'mensaje': resultado["message"]}), 201
    else:
        return jsonify({'error': resultado["error"]}), 500

@egresos_secre_bp.route('/tipos', methods=['GET'])
def listar_tipos_egreso():
    tipos = ver_tipos_egreso()
    return jsonify(tipos)

@egresos_secre_bp.route('/editar/<int:id>', methods=['PUT'])
def actualizar_egreso(id):
    data = request.json
    print("ver_egresos  data",  data)
    observacion = data.get('observacion')
    monto = data.get('monto')
    fecha = data.get('fecha')
    egreso_tipo_id = data.get('tipo')
    descartado = data.get('descartado')
    print("egreso_tipo_id", egreso_tipo_id)

    # Asegurarse de que al menos uno de los campos esté presente
    if not any([observacion, monto, fecha, egreso_tipo_id, descartado is not None]):
        return jsonify({'error': 'Faltan datos'}), 400

    resultado = editar_egreso(id, observacion, monto, fecha, egreso_tipo_id, descartado)

    if resultado["success"]:
        return jsonify({'mensaje': resultado["message"]}), 200
    else:
        return jsonify({'error': resultado["error"]}), 500

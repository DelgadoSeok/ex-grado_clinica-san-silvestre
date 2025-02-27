from flask import Blueprint, request, jsonify
from services.reportes_service import obtener_reporte_dinero_recaudado

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/reporte_dinero', methods=['GET'])
def reporte_consultas():
    return render_template('views/reporteDineros.html') 

@reportes_bp.route('/reporte_consultas', methods=['GET'])
def reporte_consultas():
    return render_template('views/reporteConsultas.html') 

@reportes_bp.route('/api/reporte_dinero', methods=['GET'])
def reporte_dinero():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    if not fecha_inicio or not fecha_fin:
        return jsonify({"success": False, "error": "Debe proporcionar fecha de inicio y fin"}), 400

    datos = obtener_reporte_dinero_recaudado(fecha_inicio, fecha_fin)
    return jsonify({"success": True, "data": datos})

@reportes_bp.route('/api/reporte_consultas', methods=['GET'])
def reporte_consultas():
    doctor_id = request.args.get('doctor_id')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    if not doctor_id or not fecha_inicio or not fecha_fin:
        return jsonify({"success": False, "error": "Debe proporcionar doctor, fecha de inicio y fin"}), 400

    datos = obtener_consultas_por_doctor(doctor_id, fecha_inicio, fecha_fin)
    return jsonify({"success": True, "data": datos})

@reportes_bp.route('/api/doctores', methods=['GET'])
def obtener_lista_doctores():
    doctores = obtener_doctores()
    return jsonify({"success": True, "data": doctores})

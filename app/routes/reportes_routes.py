from flask import Blueprint, request, jsonify
from services.reportes_service import obtener_reporte_dinero_recaudado

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/api/reporte_dinero', methods=['GET'])
def reporte_dinero():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    if not fecha_inicio or not fecha_fin:
        return jsonify({"success": False, "error": "Debe proporcionar fecha de inicio y fin"}), 400

    datos = obtener_reporte_dinero_recaudado(fecha_inicio, fecha_fin)
    return jsonify({"success": True, "data": datos})

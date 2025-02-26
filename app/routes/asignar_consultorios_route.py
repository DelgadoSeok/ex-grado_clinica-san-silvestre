from flask import Blueprint, render_template, request, jsonify
from services.asignar_consultorios_services import (
    obtener_doctores,
    obtener_consultorios_activos,
    verificar_conflicto_horario,
    asignar_consultorio,
    obtener_asignaciones_activas,
    deshabilitar_asignacion
)

asignar_consultorios_bp = Blueprint('asignar_consultorios', __name__, url_prefix='/asignar_consultorios')

@asignar_consultorios_bp.route('/', methods=['GET'])
def index():
    doctores = obtener_doctores()
    consultorios = obtener_consultorios_activos()
    asignaciones = obtener_asignaciones_activas()
    return render_template('views/asignar_consultorios.html',
                           doctores=doctores,
                           consultorios=consultorios,
                           asignaciones=asignaciones)

@asignar_consultorios_bp.route('/guardar', methods=['POST'])
def guardar_asignacion():
    doctor_id = request.form.get('doctor_id')
    dia_semana = request.form.get('dia_semana')
    hora_ini = request.form.get('hora_ini')
    hora_fin = request.form.get('hora_fin')
    consultorio_id = request.form.get('consultorio_id')
    
    # Verificar conflicto de horario
    conflicto = verificar_conflicto_horario(consultorio_id, dia_semana, hora_ini, hora_fin)
    if conflicto:
        return jsonify({'status': 'error', 'message': 'El horario se solapa con otra asignación.'})
    
    resultado = asignar_consultorio(doctor_id, dia_semana, hora_ini, hora_fin, consultorio_id)
    if resultado:
        return jsonify({'status': 'success', 'message': 'Asignación creada exitosamente.'})
    else:
        return jsonify({'status': 'error', 'message': 'Error al crear asignación.'})

@asignar_consultorios_bp.route('/deshabilitar/<int:asignacion_id>', methods=['POST'])
def inhabilitar_asignacion(asignacion_id):
    resultado = deshabilitar_asignacion(asignacion_id)
    if resultado:
        return jsonify({'status': 'success', 'message': 'Asignación inhabilitada correctamente.'})
    else:
        return jsonify({'status': 'error', 'message': 'Error al inhabilitar asignación.'})

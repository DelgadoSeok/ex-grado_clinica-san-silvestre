from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from services.consultas_service import obtener_consultas, crear_consulta, obtener_horarios_disponibles, obtener_pacientes, obtener_doctores, obtener_consultorios, verificar_disponibilidad, obtener_consulta_por_id
from reportlab.lib.pagesizes import letter
from flask import Blueprint, send_file
import io
from reportlab.pdfgen import canvas

consultas_bp = Blueprint('consultas', __name__, url_prefix='/consultas')

@consultas_bp.route('/', methods=['GET'])
def mostrar_consultas():
    # Llamar al nuevo método para obtener las deudas y mostrarlas en un log
    consultas = obtener_consultas()
    return render_template('views/consultas.html', consultas=consultas)


# recibir datos de nueva deuda que sera aplicada a todos los puestos y registrarla en db
@consultas_bp.route('/nueva_consulta', methods=['GET'])
def nueva_consulta():
    pacientes = obtener_pacientes()
    doctores = obtener_doctores()
    return render_template('views/nueva_consulta.html', pacientes=pacientes, doctores=doctores)


@consultas_bp.route('/obtener_consultorios/<int:doctor_id>', methods=['GET'])
def obtener_consultorios_route(doctor_id):
    consultorios = obtener_consultorios(doctor_id)
    return jsonify(consultorios)

consultas_bp.route('/obtener_horarios_disponibles', methods=['POST'])
def obtener_horarios_disponibles_route():
    data = request.json
    consultorio_id = data.get('consultorio_id')
    fecha = data.get('fecha')

    if not (consultorio_id and fecha):
        return jsonify({"success": False, "error": "Datos incompletos"}), 400

    horarios_disponibles = obtener_horarios_disponibles(consultorio_id, fecha)
    return jsonify({"success": True, "horarios_disponibles": horarios_disponibles})


@consultas_bp.route('/crear_consulta', methods=['POST'])
def crear_consulta_route():
    data = request.json
    paciente_id = data.get('paciente_id')
    doctor_id = data.get('doctor_id')
    consultorio_id = data.get('consultorio_id')
    fecha = data.get('fecha')
    hora_ini = data.get('hora_ini')
    tipo = data.get('tipo')

    if not (paciente_id and doctor_id and consultorio_id and fecha and hora_ini and tipo):
        return jsonify({"success": False, "error": "Datos incompletos"}), 400

    resultado = crear_consulta(paciente_id, doctor_id, consultorio_id, fecha, hora_ini, tipo)
    return jsonify(resultado)


@consultas_bp.route('/reporte/<int:consulta_id>', methods=['GET'])
def descargar_reporte(consulta_id):
    """Genera un reporte PDF de la consulta"""
    consulta = obtener_consulta_por_id(consulta_id)

    # Crear el PDF en memoria
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Reporte de Consulta")

    # Título
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Reporte de Consulta")

    # Detalles de la consulta
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 700, f"Paciente: {consulta['paciente_nombre']}")
    pdf.drawString(50, 680, f"Doctor: {consulta['doctor_nombre']}")
    pdf.drawString(50, 660, f"Consultorio: {consulta['consultorio_nro']}")
    pdf.drawString(50, 640, f"Fecha: {consulta['fecha']}")
    pdf.drawString(50, 620, f"Hora Inicio: {consulta['hora_ini']}")
    pdf.drawString(50, 600, f"Hora Fin: {consulta['hora_fin']}")
    pdf.drawString(50, 580, f"Tipo: {consulta['tipo']}")

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, mimetype='application/pdf', download_name=f"Reporte_Consulta_{consulta_id}.pdf")
import os
from flask import Blueprint, current_app, render_template, request, jsonify
from datetime import datetime
from services.consultas_service import obtener_consultas, crear_consulta, obtener_horas_inicio_consultas, obtener_pacientes, obtener_doctores, obtener_consultorios, obtener_consulta_por_id
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
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
    consultorios = obtener_consultorios()
    return jsonify({"pacientes": pacientes, "doctores": doctores, "consultorios": consultorios})

@consultas_bp.route('/hora_ini', methods=['GET'])
def hora_ini():
    fecha = request.args.get('fecha')  # Obtener la fecha desde la URL
    if fecha:
        hora_ini = obtener_horas_inicio_consultas(fecha)  # Obtener las horas disponibles para esa fecha
    else:
        hora_ini = []  # Si no se pasa la fecha, se devuelven horas vacías

    return jsonify({'hora_ini': hora_ini})

@consultas_bp.route('/crear_consulta', methods=['POST'])
def crear_consulta_route():
    data = request.json
    paciente_id = data.get('paciente_id')
    doctor_id = data.get('doctor_id')
    consultorio_id = data.get('consultorio_id')
    fecha = data.get('fecha')
    hora_ini = data.get('hora_ini')  
    hora_fin = data.get('hora_fin')  
    tipo = data.get('tipo')
    estado = data.get('estado', 'A')  

    if not (paciente_id and doctor_id and consultorio_id and fecha and hora_ini and hora_fin and tipo):
        return jsonify({"success": False, "error": "Datos incompletos"}), 400

    resultado = crear_consulta(paciente_id, doctor_id, consultorio_id, fecha, hora_ini, hora_fin, tipo, estado)
    return jsonify(resultado)


@consultas_bp.route('/reporte/<int:consulta_id>', methods=['GET'])
def descargar_reporte(consulta_id):
    """Genera un reporte PDF de la consulta"""
    consulta = obtener_consulta_por_id(consulta_id)

    # Crear el PDF en memoria
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch)
    styles = getSampleStyleSheet()

    # Contenido del PDF
    contenido = []

    # Encabezado con el logo de la clínica
    logo_path = os.path.join(current_app.root_path, 'static', 'img', 'logo_clinica.jpg')
    logo = Image(logo_path, width=2*inch, height=1*inch)
    contenido.append(logo)
    contenido.append(Spacer(1, 0.25*inch))  # Espacio después del logo

    # Título del reporte
    titulo = Paragraph("Reporte de Consulta Médica", styles['Title'])
    contenido.append(titulo)
    contenido.append(Spacer(1, 0.25*inch))  # Espacio después del título

    # Datos de la consulta en formato de tabla
    datos = [
        ["Campo", "Valor"],
        ["Paciente", consulta['paciente_nombre']],
        ["Doctor", consulta['doctor_nombre']],
        ["Consultorio", consulta['nro_consultorio']],
        ["Fecha", consulta['fecha']],
        ["Hora Inicio", consulta['hora_ini']],
        ["Hora Fin", consulta['hora_fin']],
        ["Tipo", consulta['tipo']]
    ]

    # Crear la tabla
    tabla = Table(datos, colWidths=[1.5*inch, 4*inch])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#004080")),  # Fondo azul oscuro para el encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto blanco para el encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear todo al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para el encabezado
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Tamaño de fuente para el encabezado
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior para el encabezado
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F0F0F0")),  # Fondo gris claro para las filas de datos
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Texto negro para las filas de datos
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#C0C0C0")),  # Líneas de la tabla en gris
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Fuente normal para las filas de datos
        ('FONTSIZE', (0, 1), (-1, -1), 10),  # Tamaño de fuente para las filas de datos
    ]))
    contenido.append(tabla)
    contenido.append(Spacer(1, 0.5*inch))  # Espacio después de la tabla

    # Pie de página con información de contacto
    pie_pagina = Paragraph(
        "Clínica San Silvestre<br/>"
        "Dirección: Av. Principal 123, Ciudad<br/>"
        "Teléfono: +123 456 7890<br/>"
        "Email: info@clinicasansilvestre.com",
        styles['Normal']
    )
    contenido.append(pie_pagina)

    # Construir el PDF
    pdf.build(contenido)

    # Preparar el archivo para descargar
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, mimetype='application/pdf', download_name=f"Reporte_Consulta_{consulta_id}.pdf")
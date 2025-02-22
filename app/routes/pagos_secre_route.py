from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from services.pagos_service import reporte_pagos, crear_deuda, obtener_deudas, registrar_nuevo_pago
from reportlab.lib.pagesizes import letter
from flask import Blueprint, send_file
import io
from reportlab.pdfgen import canvas
pagos_secre_bp = Blueprint('pagos_secre', __name__, url_prefix='/pagos_secre')

@pagos_secre_bp.route('/', methods=['GET'])
def mostrar_pagos():
    # Llamar al nuevo método para obtener las deudas y mostrarlas en un log
    deudas = obtener_deudas()
    return render_template('pagos_secre.html', deudas=deudas)


# recibir datos de nueva deuda que sera aplicada a todos los puestos y registrarla en db
@pagos_secre_bp.route('/crear_deudas', methods=['POST'])
def crear_deudas():
    data = request.json
    fecha = data.get("fecha", datetime.today().strftime('%Y-%m-%d'))
    monto = data.get("monto")

    if not (fecha and monto):
        print("datos erroneos")
        return jsonify({"success": False, "error": "Datos incompletos"}), 400
        
    resultado = crear_deuda(fecha, monto)
    return jsonify(resultado)

@pagos_secre_bp.route('/registrar_pago/', methods=['POST'])
def registrar_pago():
    data = request.get_json()
    deuda_id = data.get('deuda_id')
    deuda_monto = data.get('deuda_monto')
    deuda_interes = data.get('deuda_interes')

    print(f"id de fila: {deuda_id}")
    print(f"monto de fila: {deuda_monto}")
    print(f"interes de fila: {deuda_interes}")

    registrar_nuevo_pago(datetime.today().strftime('%Y-%m-%d'), deuda_monto, deuda_interes, deuda_id)
    #descargar_reporte(deuda_id)

    return jsonify(success=True)


@pagos_secre_bp.route('/reporte/<int:deuda_id>', methods=['GET'])
def descargar_reporte(deuda_id):
    """Genera un reporte PDF de pagos"""
    print(f"deuda id: {deuda_id}")
    pagos = reporte_pagos(deuda_id)  # Obtener todos los pagos

    # Crear el PDF en memoria
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Reporte de Pagos")

    # Título
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Reporte: Pago realizado y deudas pendientes")

    # Cabecera de la tabla
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, 700, "Fecha")
    pdf.drawString(150, 700, "Monto")
    pdf.drawString(250, 700, "Interés")
    pdf.drawString(350, 700, "Estado")

    y_position = 680
    pdf.setFont("Helvetica", 10)

    for pago in pagos:
        pdf.drawString(50, y_position, str(pago[0]))
        pdf.drawString(150, y_position, f"{pago[1]:,.2f}")
        pdf.drawString(250, y_position, f"{pago[2]:,.2f}" if pago[2] else "-")
        pdf.drawString(350, y_position, str(pago[3]))
        y_position -= 20

        if y_position < 50:
            pdf.showPage()
            y_position = 750

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, mimetype='application/pdf', download_name="Reporte_Pagos.pdf")

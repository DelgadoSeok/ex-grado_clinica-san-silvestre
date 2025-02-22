from flask import Blueprint, render_template, request, jsonify
from config.db import get_db_connection
from services.contratos_service import ver_contratos, editar_contrato, descartar_contrato, anular_contrato, registrar_contrato
contratos_bp = Blueprint('contratos', __name__)

@contratos_bp.route('/contratos')
def contratos():
 
    contratos = ver_contratos()
    return render_template('contratos.html', contratos=contratos)

@contratos_bp.route('/contratos/registrar', methods=['POST'])
def registrar_nuevo_contrato():
    """API para registrar un nuevo contrato"""
    try:
        data = request.json
        print("Datos recibidos para registrar contrato:", data)  # Para depuración

        resultado = registrar_contrato(
            data.get("contrato_tipo_id"),
            data.get("puesto_id"),
            data.get("fecha_ini"),
            data.get("fecha_fin"),
            data.get("monto"),
            data.get("contrato_estado_id"),
            data.get("persona1_id"),
            data.get("persona2_id"),
            data.get("descartado", 0)  # Valor por defecto si no se envía
        )

        print("Resultado del registro:", resultado)  # Depuración
        return jsonify(resultado)

    except Exception as e:
        print("Error al registrar contrato:", str(e))
        return jsonify({"success": False, "error": str(e)})


@contratos_bp.route('/contratos/editar', methods=['POST'])
def actualizar_contrato():
    """API para actualizar datos de un contrato."""
    try:
        data = request.json
        print("Datos recibidos para edición en API:", data)

        resultado = editar_contrato(
            data.get("contrato_id"),
            data.get("contrato_tipo_id") or None,
            data.get("puesto_id") or None,
            data.get("fecha_ini") or None,
            data.get("fecha_fin") or None,
            data.get("monto") or None,
            data.get("contrato_estado_id") or None,
            data.get("persona1_id") or None,
            data.get("persona2_id") or None,
            data.get("descartado") if "descartado" in data else None
        )

        print("Respuesta del servicio de edición:", resultado)
        return jsonify(resultado)

    except Exception as e:
        print("Error al actualizar contrato:", str(e))
        return jsonify({"success": False, "error": str(e)})


@contratos_bp.route('/contratos/descartar', methods=['POST'])
def descartar_un_contrato():
    """API para descartar un contrato."""
    data = request.json
    print("Solicitud para descartar contrato:", data)

    resultado = descartar_contrato(data.get("contrato_id"))
    return jsonify(resultado)

@contratos_bp.route('/contratos/anular', methods=['POST'])
def anular_un_contrato():


    """API para anular un contrato."""
    data = request.json
    print("Solicitud para anular contrato:", data)

    resultado = anular_contrato(data.get("contrato_id"))
    return jsonify(resultado)

@contratos_bp.route('/contratos/tipos')
def obtener_tipos_contrato():
    """Obtiene los tipos de contrato desde la base de datos."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.callproc("ver_tipos_contrato")

    tipos_contrato = [{"id": row[0], "descripcion": row[1]} for result in cursor.stored_results() for row in result.fetchall()]
    
    cursor.close()
    db.close()
    return jsonify(tipos_contrato)


@contratos_bp.route('/contratos/puestos')
def obtener_puestos():
    """Obtiene los puestos disponibles."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.callproc("ver_puestos")

    puestos = [{"id": row[0], "descripcion": f"Puesto {row[1]}"} for result in cursor.stored_results() for row in result.fetchall()]
    
    cursor.close()
    db.close()
    return jsonify(puestos)


@contratos_bp.route('/contratos/estados')
def obtener_estados_contrato():
    """Obtiene los estados del contrato."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.callproc("ver_contrato_estado")

    estados = [{"id": row[0], "descripcion": row[1]} for result in cursor.stored_results() for row in result.fetchall()]
    cursor.close()
    db.close()
    return jsonify(estados)

@contratos_bp.route('/contratos/personas')
def obtener_personas():
    """Obtiene las personas disponibles."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.callproc("ver_personas")

    personas = [{"id": row[0], "descripcion": row[1]} for result in cursor.stored_results() for row in result.fetchall()]
    
    cursor.close()
    db.close()
    return jsonify(personas)


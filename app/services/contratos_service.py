from config.db import get_db_connection

def ver_contratos():
    """Obtiene la lista de contratos desde la base de datos usando `ver_contratos`."""
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.callproc("ver_contratos")  # Llamar al procedimiento almacenado

        contratos = []
        for result in cursor.stored_results():
            for row in result.fetchall():
                contratos.append({
                    "contrato_id": row[0],
                    "tipo_contrato": row[1],
                    "puesto": row[2],
                    "fecha_ini": row[3],
                    "fecha_fin": row[4],
                    "monto": row[5],
                    "estado_contrato": row[6],
                    "vendedor_dueno": row[7],
                    "comprador_inquilino": row[8],
                    "descartado": row[9]
                })

        cursor.close()
        db.close()

        return contratos

    except Exception as e:
        print(f"Error al obtener contratos: {str(e)}")
        return []
    
def editar_contrato(contrato_id, contrato_tipo_id=None, puesto_id=None, fecha_ini=None, fecha_fin=None, monto=None, contrato_estado_id=None, persona1_id=None, persona2_id=None, descartado=None):
    """ Llama al procedimiento almacenado `editar_contrato` para modificar un contrato """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        print("Datos enviados a MySQL para edición:", contrato_id, contrato_tipo_id, puesto_id, fecha_ini, fecha_fin, monto, contrato_estado_id, persona1_id, persona2_id, descartado)

        cursor.callproc("editar_contrato", (
            contrato_id, 
            contrato_tipo_id if contrato_tipo_id else None, 
            puesto_id if puesto_id else None, 
            fecha_ini if fecha_ini else None, 
            fecha_fin if fecha_fin else None, 
            monto if monto else None, 
            contrato_estado_id if contrato_estado_id else None, 
            persona1_id if persona1_id else None, 
            persona2_id if persona2_id else None, 
            descartado if descartado is not None else None
        ))

        db.commit()
        cursor.close()
        db.close()

        return {"success": True, "message": "Contrato actualizado correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}

def descartar_contrato(contrato_id):
    """Descarta un contrato usando el procedimiento almacenado `descartar_contrato`."""
    try:
        db = get_db_connection()
        cursor = db.cursor()

        print(f"Descartando contrato con ID: {contrato_id}")

        cursor.callproc("descartar_contrato", (contrato_id,))
        db.commit()

        cursor.close()
        db.close()

        return {"success": True, "message": "Contrato descartado correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}
def anular_contrato(contrato_id):
    """Anula un contrato cambiando su estado a inactivo usando `anular_contrato`."""
    try:
        db = get_db_connection()
        cursor = db.cursor()

        print(f"Anulando contrato con ID: {contrato_id}")

        cursor.callproc("anular_contrato", (contrato_id,))
        db.commit()

        cursor.close()
        db.close()

        return {"success": True, "message": "Contrato anulado correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}
def registrar_contrato(contrato_tipo_id, puesto_id, fecha_ini, fecha_fin, monto, contrato_estado_id, persona1_id, persona2_id, descartado):
    """ Llama al procedimiento almacenado `crear_contrato` para registrar un contrato """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        print("Datos enviados a MySQL:", contrato_tipo_id, puesto_id, fecha_ini, fecha_fin, monto, contrato_estado_id, persona1_id, persona2_id, descartado)

        cursor.callproc("crear_contrato", (
            contrato_tipo_id, puesto_id, fecha_ini, fecha_fin, monto,
            contrato_estado_id, persona1_id, persona2_id, descartado
        ))
        db.commit()

        cursor.close()
        db.close()
        return {"success": True, "message": "Contrato registrado correctamente"}

    except Exception as e:
        print("Error en MySQL al registrar contrato:", str(e))
        return {"success": False, "error": str(e)}

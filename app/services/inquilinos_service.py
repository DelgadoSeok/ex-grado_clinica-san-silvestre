from config.db import get_db_connection

def obtener_inquilinos():
    """ Obtiene los inquilinos registrados en la base de datos """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Usar el procedimiento correcto para inquilinos
        cursor.execute("CALL ver_inquilino()")
        inquilinos = cursor.fetchall()

        cursor.close()
        db.close()
        return inquilinos

    except Exception as e:
        print(f"Error al obtener inquilinos: {str(e)}")
        return []

def registrar_inquilino(nombres, apellidos, ci, telf, direccion):
    """ Llama al procedimiento almacenado `crear_inquilino` para registrar un inquilino """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        print(f"Registrando: {nombres}, {apellidos}, {ci}, {telf}, {direccion}")  # Depuración

        cursor.callproc("crear_inquilino", (nombres, apellidos, ci, telf, direccion))

        db.commit()
        cursor.close()
        db.close()
        return {"success": True, "message": "Inquilino registrado correctamente"}
    except Exception as e:
        print("Error en registro:", e)
        return {"success": False, "error": str(e)}

def editar_inquilino(id, nombres, apellidos, ci, telf, direccion):
    """ Llama al procedimiento almacenado `editar_inquilino` para modificar un inquilino """
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Enviamos `None` para los valores opcionales de estado, tipo y descartado
        cursor.callproc("editar_inquilino", (id, nombres, apellidos, ci, telf, direccion, None, 2, None))
        
        db.commit()
        cursor.close()
        db.close()
        return {"success": True, "message": "Inquilino actualizado correctamente"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def descartar_inquilino(id):
    """ Llama al procedimiento almacenado `descartar_persona` para descartar un inquilino """
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.callproc("descartar_persona", (id,))
        db.commit()
        cursor.close()
        db.close()
        return {"success": True, "message": "Inquilino descartado correctamente"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    

def obtener_id_inquilino(inquilino_nombre=None):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        if inquilino_nombre:
            cursor.execute("""
                SELECT id 
                FROM persona 
                WHERE nombres = %s 
                AND persona_tipo_id = (SELECT id FROM persona_tipo_id WHERE descripcion = 'Inquilino')
            """, (inquilino_nombre,))
        else:
            cursor.execute("""
                SELECT id, nombres 
                FROM persona 
                WHERE persona_tipo_id = (SELECT id FROM persona_tipo_id WHERE descripcion = 'Inquilino')
            """)  # Obtener solo los Inqulinos
        
        resultado = cursor.fetchall() if not inquilino_nombre else cursor.fetchone()
        cursor.close()
        db.close()
        
        # Si se pide un inquilino específico, devuelve el ID
        if inquilino_nombre:
            return resultado['id'] if resultado else None
        # Si no, devuelve una lista de inquilinos
        return resultado if resultado else []
    except Exception as e:
        print(f"Error al obtener el inquilino: {e}")
        return None

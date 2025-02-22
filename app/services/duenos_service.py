from config.db import get_db_connection

def ver_duenos():
    """ Obtiene la lista de dueños desde el procedimiento almacenado `ver_dueno` """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.callproc("ver_dueno")  # Llamar al procedimiento almacenado

        # Obtener resultados
        duenos = []
        for result in cursor.stored_results():  # IMPORTANTE: obtener los resultados correctamente
            for row in result.fetchall():
                duenos.append({
                    "id": row[0],
                    "nombres": row[1],
                    "apellidos": row[2],
                    "ci": row[3],
                    "telefono": row[4],
                    "direccion": row[5]
                })

        cursor.close()
        db.close()

        print("Dueños obtenidos:", duenos)  # Depuración en la consola

        return duenos

    except Exception as e:
        print(f"Error al obtener dueños: {str(e)}")
        return []

def registrar_dueno(nombres, apellidos, ci, telf, direccion):
    """ Registra un nuevo dueño usando el procedimiento almacenado `registrar_dueno` """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.callproc("registrar_dueno", (nombres, apellidos, ci, telf, direccion))
        db.commit()

        cursor.close()
        db.close()
        return {"success": True, "message": "Dueño registrado correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}

def editar_dueno(dueno_id, nombres, apellidos, ci, telf, direccion):
    """ Edita los datos de un dueño usando el procedimiento almacenado `editar_dueno` """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        print("Datos enviados a MySQL:", dueno_id, nombres, apellidos, ci, telf, direccion)  # Para depuración

        cursor.callproc("editar_dueno", (dueno_id, nombres or "", apellidos or "", ci or "", telf or "", direccion or ""))

        db.commit()
        cursor.close()
        db.close()

        return {"success": True, "message": "Datos del dueño actualizados correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}

def descartar_dueno(dueno_id):
    """ Llama al procedimiento almacenado `descartar_persona` para marcar un dueño como descartado. """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        print(f"Descartando dueño con ID: {dueno_id}")  # Para depuración

        cursor.callproc("descartar_persona", (dueno_id,))
        db.commit()

        cursor.close()
        db.close()

        return {"success": True, "message": "Dueño descartado correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}

def obtener_id_dueno(dueno_nombre=None):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Si se pasa un nombre, buscarlo, sino obtener todos los dueños
        if dueno_nombre:
            cursor.execute("""
                SELECT id 
                FROM persona 
                WHERE nombres = %s 
                AND persona_tipo_id = (SELECT id FROM persona_tipo_id WHERE descripcion = 'Dueño')
            """, (dueno_nombre,))
        else:
            cursor.execute("""
                SELECT id, nombres 
                FROM persona 
                WHERE persona_tipo_id = (SELECT id FROM persona_tipo_id WHERE descripcion = 'Dueño')
            """)  # Obtener solo los dueños
        
        resultado = cursor.fetchall() if not dueno_nombre else cursor.fetchone()
        cursor.close()
        db.close()
        
        # Si se pide un dueño específico, devuelve el ID
        if dueno_nombre:
            return resultado['id'] if resultado else None
        # Si no, devuelve una lista de dueños
        return resultado if resultado else []
    except Exception as e:
        print(f"Error al obtener el dueño: {e}")
        return None

from config.db import get_db_connection

def obtener_puestos():
    """ Obtiene los puestos registrados en la base de datos """
    try:
        db = get_db_connection()
        cursor = db.cursor()  

        cursor.execute("CALL ver_puestos()")
        puestos = cursor.fetchall()

        cursor.close()
        db.close()
        return puestos

    except Exception as e:
        print(f"Error al obtener puestos: {str(e)}")
        return []
    

def registrar_puesto( numero, asociacion, gremio, sector, estado, dueno, inquilino,):
    try:
        db = get_db_connection()
        cursor = db.cursor()
 
        # Crear una tupla con los parámetros
        parametros = (numero, asociacion, gremio, sector, estado, dueno, inquilino)
        cursor.callproc('registrar_puesto',  parametros)
        db.commit()
        cursor.close()
        db.close()
        return {"success": True, "message": "Puesto registrado correctamente"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def ver_puesto(p_numero=None, p_asociacion_descripcion=None, p_sector_descripcion=None, p_puesto_estado_descripcion=None, p_gremio_descripcion=None, p_puesto_estado_id=None, p_dueno_id=None, p_inquilino_id=None, p_dueno_nombre=None, p_inquilino_nombre=None):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        # Llamada al procedimiento almacenado
        cursor.callproc(
            'ver_puestos', 
        )
        puestos = []
        for result in cursor.stored_results():
            puestos = result.fetchall()

        cursor.close()
        db.close()
        return puestos
    except Exception as e:
        return {"success": False, "error": str(e)}


def editar_puesto(id, data):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.callproc('editar_puesto', [id, data['numero'], data['asociacion_id'], data['gremio_id'], data['sector_id'], data['puesto_estado_id'], data['dueno_id'], data['inquilino_id']])
        db.commit()
        cursor.close()
        db.close()
        return {"success": True, "message": "Datos del puesto actualizados correctamente"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Función para obtener el ID del puesto_estado
def obtener_id_puesto_estado(estado_nombre):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id FROM puesto_estado WHERE descripcion = %s", (estado_nombre,))
        resultado = cursor.fetchone()
        cursor.close()
        db.close()
        return resultado['id'] if resultado else None
    except Exception as e:
        print(f"Error al obtener el estado del puesto: {e}")
        return None



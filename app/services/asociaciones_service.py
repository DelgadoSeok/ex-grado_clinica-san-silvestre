from config.db import get_db_connection

# Función para obtener el ID de la asociación
def obtener_id_asociacion(asociacion_nombre=None):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        if asociacion_nombre:
            cursor.execute("SELECT id FROM asociacion WHERE descripcion = %s", (asociacion_nombre,))
        else:
            cursor.execute("SELECT id, descripcion FROM asociacion")  # Retorna todas las asociaciones
        
        resultado = cursor.fetchall() if not asociacion_nombre else cursor.fetchone()
        cursor.close()
        db.close()
        
        # Si se pidió una asociación específica, devuelve el ID
        if asociacion_nombre:
            return resultado['id'] if resultado else None
        # Si no, devuelve una lista de asociaciones
        return resultado if resultado else []
    except Exception as e:
        print(f"Error al obtener la asociación: {e}")
        return None
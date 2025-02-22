from config.db import get_db_connection

# Función para obtener el ID del gremio
def obtener_id_gremio(gremio_nombre=None):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        if gremio_nombre:
            cursor.execute("SELECT id FROM gremio WHERE descripcion = %s", (gremio_nombre,))
        else:
            cursor.execute("SELECT id, descripcion FROM gremio")  # Obtener todos los gremios
        
        resultado = cursor.fetchall() if not gremio_nombre else cursor.fetchone()
        cursor.close()
        db.close()
        
        # Si se pide un gremio específico, devuelve el ID
        if gremio_nombre:
            return resultado['id'] if resultado else None
        # Si no, devuelve una lista de gremios
        return resultado if resultado else []
    except Exception as e:
        print(f"Error al obtener el gremio: {e}")
        return None

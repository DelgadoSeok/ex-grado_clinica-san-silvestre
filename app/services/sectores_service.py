from config.db import get_db_connection
# Función para obtener el ID del sector
def obtener_id_sector(sector_nombre=None):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        if sector_nombre:
            cursor.execute("SELECT id FROM sector WHERE descripcion = %s", (sector_nombre,))
        else:
            cursor.execute("SELECT id, descripcion FROM sector")  # Obtener todos los sectores
        
        resultado = cursor.fetchall() if not sector_nombre else cursor.fetchone()
        cursor.close()
        db.close()
        
        # Si se pide un sector específico, devuelve el ID
        if sector_nombre:
            return resultado['id'] if resultado else None
        # Si no, devuelve una lista de sectores
        return resultado if resultado else []
    except Exception as e:
        print(f"Error al obtener el sector: {e}")
        return None

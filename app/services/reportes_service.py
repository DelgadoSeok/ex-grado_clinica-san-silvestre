from config.db import get_db_connection

def obtener_reporte_dinero_recaudado(fecha_inicio, fecha_fin):
    """Obtiene el dinero recaudado en un intervalo de tiempo"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        query = """
            SELECT 
            	cons.id,
            	per.nombres,
                per.p_apellido,
                per.s_apellido,
            	cons.fecha, 
            	cons.hora_ini, 
            	cons.importe
            FROM consulta as cons, persona as per
            WHERE cons.paciente_id = per.id 
            AND cons.fecha BETWEEN %s AND %s
            ORDER BY fecha ASC, hora_ini ASC
        """
        cursor.execute(query, (fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()

        cursor.close()
        db.close()
        
        return resultados
    except Exception as e:
        print(f"Error al obtener el reporte: {str(e)}")
        return []

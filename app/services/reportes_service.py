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
            FROM consulta AS cons, persona AS per
            WHERE cons.paciente_id = per.id 
            AND cons.fecha BETWEEN %s AND %s
            ORDER BY cons.fecha ASC, cons.hora_ini ASC
        """
        
        cursor.execute(query, (fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()

        # Formatear los datos para incluir el nombre completo del paciente
        for row in resultados:
            row["paciente"] = f"{row['nombres']} {row['p_apellido']} {row['s_apellido']}".strip()
            del row["nombres"], row["p_apellido"], row["s_apellido"]  # Eliminamos campos innecesarios

        cursor.close()
        db.close()
        
        return resultados
    except Exception as e:
        print(f"Error al obtener el reporte: {str(e)}")
        return []

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

def obtener_consultas_por_doctor(doctor_id, fecha_inicio, fecha_fin):
    """Obtiene las consultas de un doctor en un intervalo de tiempo sin SP"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT 
                cons.id,
                per.nombres + ' ' + per.p_apellido + ' ' + per.s_apellido AS paciente,
                cons.fecha,
                cons.hora_ini,
                cons.importe
            FROM consulta AS cons
            INNER JOIN persona AS per ON cons.paciente_id = per.id
            WHERE cons.doctor_id = %s
            AND cons.fecha BETWEEN %s AND %s
            ORDER BY cons.fecha ASC, cons.hora_ini ASC
        """
        cursor.execute(query, (doctor_id, fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()

        cursor.close()
        db.close()
        
        return resultados
    except Exception as e:
        print(f"Error al obtener las consultas: {str(e)}")
        return []

def obtener_doctores():
    """Obtiene la lista de doctores"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        query = "SELECT id, nombres, p_apellido, s_apellido FROM persona WHERE rol = 'doctor'"
        cursor.execute(query)
        doctores = cursor.fetchall()

        cursor.close()
        db.close()

        return doctores
    except Exception as e:
        print(f"Error al obtener doctores: {str(e)}")
        return []

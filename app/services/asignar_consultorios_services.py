from config.db import get_db_connection
import os
from dotenv import load_dotenv
load_dotenv()

def obtener_doctores():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM doctor WHERE estado = 'A'"
    cursor.execute(query)
    doctores = cursor.fetchall()
    cursor.close()
    connection.close()
    return doctores

def obtener_consultorios_activos():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM consultorio WHERE estado = 'A'"
    cursor.execute(query)
    consultorios = cursor.fetchall()
    cursor.close()
    connection.close()
    return consultorios

def verificar_conflicto_horario(consultorio_id, dia_semana, hora_ini, hora_fin):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT * FROM asignacion_consultorio
    WHERE consultorio_id = %s AND dia_semana = %s AND estado = 'A'
      AND (hora_ini < %s AND hora_fin > %s)
    """
    # Se pasa hora_fin y hora_ini del nuevo intervalo para detectar cualquier solapamiento
    cursor.execute(query, (consultorio_id, dia_semana, hora_fin, hora_ini))
    resultado = cursor.fetchone()
    cursor.close()
    connection.close()
    return resultado is not None

def asignar_consultorio(doctor_id, dia_semana, hora_ini, hora_fin, consultorio_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO asignacion_consultorio (doctor_id, dia_semana, hora_ini, hora_fin, consultorio_id, estado)
        VALUES (%s, %s, %s, %s, %s, 'A')
        """
        cursor.execute(query, (doctor_id, dia_semana, hora_ini, hora_fin, consultorio_id))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print("Error asignando consultorio:", e)
        return False

def obtener_asignaciones_activas():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT ac.id, d.matricula_profesional, ac.dia_semana, ac.hora_ini, ac.hora_fin, c.nro_consultorio
    FROM asignacion_consultorio ac
    JOIN doctor d ON ac.doctor_id = d.id
    JOIN consultorio c ON ac.consultorio_id = c.id
    WHERE ac.estado = 'A'
    """
    cursor.execute(query)
    asignaciones = cursor.fetchall()
    cursor.close()
    connection.close()
    return asignaciones

def deshabilitar_asignacion(asignacion_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "UPDATE asignacion_consultorio SET estado = 'I' WHERE id = %s"
        cursor.execute(query, (asignacion_id,))
        connection.commit()
        affected = cursor.rowcount  # número de filas afectadas
        cursor.close()
        connection.close()
        if affected == 0:
            print("No se actualizó ninguna fila para id:", asignacion_id)
            return False
        return True
    except Exception as e:
        print("Error inhabilitando asignacion:", e)
        return False

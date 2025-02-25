from config.db import get_db_connection
from datetime import datetime, time, timedelta

def obtener_consultas():
    """Obtiene todas las consultas ordenadas por fecha descendente"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, 
                CONCAT(pp.nombres, ' ', pp.p_apellido, ' ', pp.s_apellido) AS paciente_nombre,
                CONCAT(pd.nombres, ' ', pd.p_apellido, ' ', pd.s_apellido) AS doctor_nombre,
                co.nro_consultorio
            FROM consulta c
            JOIN persona pp ON c.paciente_id = pp.id
            JOIN doctor d ON c.doctor_id = d.id
            JOIN persona pd ON d.id = pd.id
            JOIN consultorio co ON c.consultorio_id = co.id
            ORDER BY c.fecha DESC, c.hora_ini DESC
        """)
        consultas = cursor.fetchall()
        cursor.close()
        db.close()
        print(consultas)
        return consultas
    except Exception as e:
        print(f"Error al obtener consultas: {str(e)}")
        return []


def obtener_pacientes():
    """Obtiene la lista de pacientes"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, CONCAT(nombres, ' ', p_apellido, ' ', s_apellido) AS nombre_completo
            FROM persona
            WHERE estado = 'A'
        """)
        pacientes = cursor.fetchall()
        cursor.close()
        db.close()
        return pacientes
    except Exception as e:
        print(f"Error al obtener pacientes: {str(e)}")
        return []


def obtener_doctores():
    """Obtiene la lista de doctores disponibles"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, CONCAT(nombres, ' ', p_apellido, ' ', s_apellido) AS nombre_completo
            FROM persona
            WHERE estado = 'A'
        """)
        doctores = cursor.fetchall()
        cursor.close()
        db.close()
        return doctores
    except Exception as e:
        print(f"Error al obtener doctores: {str(e)}")
        return []


def obtener_consultorios(doctor_id):
    """Obtiene la lista de consultorios disponibles para un doctor"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nro_consultorio FROM consultorio WHERE estado = 'A'")
        consultorios = cursor.fetchall()
        cursor.close()
        db.close()
        return consultorios
    except Exception as e:
        print(f"Error al obtener consultorios: {str(e)}")
        return []


def verificar_disponibilidad(consultorio_id, fecha, hora_ini, hora_fin):
    """verifica si el consultorio está disponible en la fecha y hora especificadas"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM consulta 
            WHERE consultorio_id = %s 
            AND fecha = %s 
            AND ((hora_ini < %s AND hora_fin > %s) OR (hora_ini < %s AND hora_fin > %s))
        """, (consultorio_id, fecha, hora_fin, hora_ini, hora_ini, hora_fin))
        consulta = cursor.fetchone()
        cursor.close()
        db.close()
        return consulta is None
    except Exception as e:
        print(f"Error al verificar disponibilidad: {str(e)}")
        return False


def obtener_horarios_disponibles(consultorio_id, fecha):
    """Obtiene los horarios disponibles en intervalos de 20 minutos para un consultorio en una fecha específica."""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Obtener las consultas existentes para el consultorio en la fecha especificada
        cursor.execute("""
            SELECT hora_ini, hora_fin 
            FROM consulta 
            WHERE consultorio_id = %s AND fecha = %s
        """, (consultorio_id, fecha))
        consultas = cursor.fetchall()

        # Definir el horario de trabajo (por ejemplo, de 8:00 a 18:00)
        horario_inicio = time(8, 0)  # 8:00 AM
        horario_fin = time(18, 0)    # 6:00 PM

        # Generar todos los intervalos de 20 minutos en el horario de trabajo
        intervalos = []
        tiempo_actual = datetime.combine(datetime.today(), horario_inicio)
        while tiempo_actual.time() <= horario_fin:
            intervalos.append(tiempo_actual.time())
            tiempo_actual += timedelta(minutes=20)

        # Filtrar los intervalos que no están ocupados por consultas existentes
        horarios_disponibles = []
        for intervalo in intervalos:
            disponible = True
            intervalo_ini = intervalo
            intervalo_fin = (datetime.combine(datetime.today(), intervalo) + timedelta(minutes=20)).time()

            for consulta in consultas:
                if not (intervalo_fin <= consulta['hora_ini'] or intervalo_ini >= consulta['hora_fin']):
                    disponible = False
                    break

            if disponible:
                horarios_disponibles.append(intervalo_ini.strftime('%H:%M'))

        cursor.close()
        db.close()
        return horarios_disponibles
    except Exception as e:
        print(f"Error al obtener horarios disponibles: {str(e)}")
        return []


def crear_consulta(paciente_id, doctor_id, consultorio_id, fecha, hora_ini,tipo):
    """Crea una nueva consulta"""
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Verificar que la hora_ini esté en un intervalo válido (cada 20 minutos)
        hora_ini_time = datetime.strptime(hora_ini, '%H:%M').time()
        minutos = hora_ini_time.minute
        if minutos not in [0, 20]:
            return {"success": False, "error": "El horario debe ser en intervalos de 20 minutos."}

        # Calcular hora_fin (20 minutos después de hora_ini)
        hora_fin_time = (datetime.combine(datetime.today(), hora_ini) + timedelta(minutes=20)).time()

        # Verificar disponibilidad del horario
        disponible = verificar_disponibilidad(consultorio_id, fecha, hora_ini, hora_fin_time)
        if not disponible:
            return {"success": False, "error": "El horario seleccionado no está disponible."}

        cursor.execute("""
            INSERT INTO consulta (paciente_id, doctor_id, consultorio_id, fecha, hora_ini, hora_fin, tipo, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'A')
        """, (paciente_id, doctor_id, consultorio_id, fecha, hora_ini_time, hora_fin_time, tipo))
        db.commit()
        consulta_id = cursor.lastrowid
        cursor.close()
        db.close()
        return {"success": True, "consulta_id": consulta_id}
    except Exception as e:
        print(f"Error al crear consulta: {str(e)}")
        return {"success": False, "error": str(e)}


def obtener_consulta_por_id(consulta_id):
    """Obtiene los detalles de una consulta por su ID"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, 
                CONCAT(pp.nombres, ' ', pp.p_apellido, ' ', pp.s_apellido) AS paciente_nombre,
                CONCAT(pd.nombres, ' ', pd.p_apellido, ' ', pd.s_apellido) AS doctor_nombre,
                co.nro_consultorio
            FROM consulta c
            JOIN persona pp ON c.paciente_id = pp.id
            JOIN doctor d ON c.doctor_id = d.id
            JOIN persona pd ON d.id = pd.id
            JOIN consultorio co ON c.consultorio_id = co.id
            WHERE c.id = %s
        """, (consulta_id,))
        consulta = cursor.fetchone()
        cursor.close()
        db.close()
        return consulta
    except Exception as e:
        print(f"Error al obtener consulta: {str(e)}")
        return None
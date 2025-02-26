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
            SELECT p.id, CONCAT(p.nombres, ' ', p.p_apellido, ' ', p.s_apellido) AS nombre_completo
            FROM persona p
            INNER JOIN paciente pa ON pa.id = p.id  # Nos aseguramos de que exista un registro en la tabla paciente
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
            SELECT p.id, CONCAT(p.nombres, ' ', p.p_apellido, ' ', p.s_apellido) AS nombre_completo
            FROM persona p
            INNER JOIN doctor d ON d.id = p.id
            WHERE d.estado = 'A'
        """)
        doctores = cursor.fetchall()
        cursor.close()
        db.close()
        return doctores
    except Exception as e:
        print(f"Error al obtener doctores: {str(e)}")
        return []


def obtener_consultorios():
    """Obtiene la lista de todos los consultorios disponibles"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, nro_consultorio
            FROM consultorio
            WHERE estado = 'A'
        """)
        consultorios = cursor.fetchall()
        
        cursor.close()
        db.close()
        return consultorios
    except Exception as e:
        print(f"Error al obtener consultorios: {str(e)}")
        return []

def generar_lista_horas():
    horas = []
    hora_inicial = datetime.strptime('08:00:00', '%H:%M:%S')
    hora_final = datetime.strptime('18:00:00', '%H:%M:%S')
    intervalo = timedelta(minutes=20)
    
    while hora_inicial <= hora_final:
        horas.append(hora_inicial.strftime('%H:%M:%S'))
        hora_inicial += intervalo
    
    return horas

def obtener_horas_inicio_consultas(fecha):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = "SELECT hora_ini FROM consulta WHERE estado = 'A' AND fecha = %s"
    cursor.execute(query, (fecha,))
    resultados = cursor.fetchall()
    
    horas_inicio = [
        (consulta['hora_ini'].total_seconds() // 3600,  # horas
         (consulta['hora_ini'].total_seconds() % 3600) // 60)  # minutos
        for consulta in resultados
    ]
    
    # Formateamos las horas y minutos en formato 'HH:MM:SS'
    horas_inicio = [f'{int(hora):02}:{int(minuto):02}:00' for hora, minuto in horas_inicio]
    
    # Generar la lista de horas posibles entre las 08:00:00 y las 18:00:00 con intervalos de 30 minutos
    hora_ini = []
    hora_inicial = datetime.strptime('08:00:00', '%H:%M:%S')
    hora_final = datetime.strptime('18:00:00', '%H:%M:%S')
    intervalo = timedelta(minutes=30)
    
    
    while hora_inicial <= hora_final:
        hora_formateada = hora_inicial.strftime('%H:%M:%S')
        # Añadir a la lista solo si la hora no está ocupada
        if hora_formateada not in horas_inicio:
            hora_ini.append(hora_formateada)
        hora_inicial += intervalo
    
    cursor.close()
    
    return hora_ini

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

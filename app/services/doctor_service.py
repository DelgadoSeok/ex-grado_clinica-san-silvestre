from config.db import get_db_connection


def ver_doctores():
    """ Obtiene la lista de doctores desde la base de datos """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        consulta = """
        SELECT 
            d.id AS id,
            CONCAT_WS(' ',p.nombres,p.p_apellido,p.s_apellido) nombre,
            p.nombres,
            p.p_apellido,
            p.s_apellido,
            p.fecha_nacimiento,
            p.email,
            p.direccion,
            -- concatenar todas las especialidades agrupadas del doctor
            IFNULL(GROUP_CONCAT(e.descripcion SEPARATOR ', '), 'Ninguna') AS especialidad,
            p.sexo,
            p.ci,
            d.matricula_profesional,
            d.estado
        FROM doctor d
        INNER JOIN persona p ON p.id = d.id
        LEFT JOIN doctor_especialidad de ON de.doctor_id = d.id
        LEFT JOIN especialidad e ON e.id = de.especialidad_id
        -- agrupar por id de doctor
        GROUP BY d.id;

        """
        
        cursor.execute(consulta)  # Ejecutar consulta SQL

         # Obtener nombres de columnas de manera dinámica
        columnas = [desc[0] for desc in cursor.description]

        # Obtener resultados y construir lista de diccionarios
        doctores = []
        for row in cursor.fetchall():
            doctores.append(dict(zip(columnas, row)))  # Empareja cada columna con su valor en la fila

        cursor.close()
        db.close()
        return doctores

    except Exception as e:
        print(f"Error al obtener doctores: {str(e)}")
        return []


# agregar datos a la tabla persona
def registrar_persona(data):

    try:
        db = get_db_connection()
        cursor = db.cursor()

        consulta = """
        INSERT INTO persona (nombres, p_apellido, s_apellido, fecha_nacimiento, sexo, ci, email, direccion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            data['nombres'],
            data['pApellido'],
            data['sApellido'],
            data['fechaNacimiento'],
            data['sexo'],
            data['ci'],
            data['email'],
            data['direccion']
        )
        
        cursor.execute(consulta, valores)  # Ejecutar consulta SQL
        db.commit()  # Confirmar la transacción

        # Obtener el ID de la persona recién insertada
        cursor.execute("SELECT LAST_INSERT_ID()")
        persona_id = cursor.fetchone()[0]

        cursor.close()
        db.close()
        return {"success": True, "message": "Persona registrada correctamente", "persona_id": persona_id}

    except Exception as e:
        return {"success": False, "error": str(e)}

# actualizar datos en la tabla persona
def editar_persona(data):

    try:
        db = get_db_connection()
        cursor = db.cursor()

        consulta = """
        UPDATE persona
        SET nombres = %s, p_apellido = %s, s_apellido = %s, fecha_nacimiento = %s, sexo = %s, ci = %s, email = %s, direccion = %s
        WHERE id = %s
        """

        valores = (
            data['nombres'],
            data['pApellido'],
            data['sApellido'],
            data['fechaNacimiento'],
            data['sexo'],
            data['ci'],
            data['email'],
            data['direccion'],
            data['doctorId']
        )
        
        cursor.execute(consulta, valores)  # Ejecutar consulta SQL
        db.commit()  # Confirmar la transacción

        cursor.close()
        db.close()
        return {"success": True, "message": "Datos de paciente actualizados correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}

# agregar datos a la tabla doctor
def registrar_doctor(data, persona_id):

    try:
        db = get_db_connection()
        cursor = db.cursor()

        consulta = """
        INSERT INTO doctor (id, matricula_profesional)
        VALUES (%s, %s)
        """

        valores = (
            persona_id,
            data['matricula']
        )
        
        cursor.execute(consulta, valores)  # Ejecutar consulta SQL
        db.commit()  # Confirmar la transacción

        cursor.close()
        db.close()
        return {"success": True, "message": "Persona registrada correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}


# agregar datos a la tabla hirotial_doctor (ingreso o retiro)
def registrar_historial_doctor(doctor_id, fecha_registro, evento):

    try:
        db = get_db_connection()
        cursor = db.cursor()

        consulta = """
        INSERT INTO doctor_historial (doctor_id, fecha_registro, evento)
        VALUES (%s, %s, %s)
        """

        valores = (
            doctor_id,
            fecha_registro,
            evento
        )
        
        cursor.execute(consulta, valores)  # Ejecutar consulta SQL
        db.commit()  # Confirmar la transacción

        cursor.close()
        db.close()
        return {"success": True, "message": "Evento de doctor registrado en historial de doctor correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}


# agregar datos a la tabla telefono
def registrar_telefono(persona_id, nro_telefonico):

    try:
        db = get_db_connection()
        cursor = db.cursor()

        consulta = """
        INSERT INTO telefono (persona_id, nro_telefono)
        VALUES (%s, %s)
        """

        valores = (
            persona_id,
            nro_telefonico
        )
        
        cursor.execute(consulta, valores)  # Ejecutar consulta SQL
        db.commit()  # Confirmar la transacción

        cursor.close()
        db.close()
        return {"success": True, "message": "Telefono registrado correctamente"}

    except Exception as e:
        print({"success": False, "error": str(e)})
        return {"success": False, "error": str(e)}


def ver_especialidades():

    try:
        db = get_db_connection()
        cursor = db.cursor()

        consulta = """
        SELECT 
            id,
            descripcion
        FROM especialidad;
        """
        
        cursor.execute(consulta)  # Ejecutar consulta SQL

         # Obtener nombres de columnas de manera dinámica
        columnas = [desc[0] for desc in cursor.description]

        # Obtener resultados y construir lista de diccionarios
        especialidades = []
        for row in cursor.fetchall():
            especialidades.append(dict(zip(columnas, row)))  # Empareja cada columna con su valor en la fila

        cursor.close()
        db.close()
        return especialidades

    except Exception as e:
        print(f"Error al obtener especialidades: {str(e)}")
        return []

# agregar datos a la tabla doctor_especialidad
def registrar_doctor_especialidad(doctor_id, especialidad_id):

    try:
        db = get_db_connection()
        cursor = db.cursor()

        consulta = """
        INSERT INTO doctor_especialidad (doctor_id, especialidad_id)
        VALUES (%s, %s)
        """

        valores = (
            doctor_id,
            especialidad_id
        )
        
        cursor.execute(consulta, valores)  # Ejecutar consulta SQL
        db.commit()  # Confirmar la transacción

        cursor.close()
        db.close()
        return {"success": True, "message": "Especialidad agregada a doctor correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}
    

# cambiar el estado del doctor
def cambiar_estado(doctor_id, nuevo_estado):

    try:
        db = get_db_connection()
        cursor = db.cursor()

        consulta = """
        UPDATE doctor
        SET estado = %s
        WHERE id = %s
        """

        valores = (
            nuevo_estado,
            doctor_id
            
        )
        
        cursor.execute(consulta, valores)  # Ejecutar consulta SQL
        db.commit()  # Confirmar la transacción

        cursor.close()
        db.close()
        return {"success": True, "message": "Estado de doctor cambiado correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}


# inactivar las asignaciones de consultorio del doctor indicado (descartar asignaciones, los consultorios quedan libres)
def inactivar_asignaciones_consultorios(doctor_id):

    try:
        db = get_db_connection()
        cursor = db.cursor()

        consulta = """
        UPDATE asignacion_consultorio
        SET estado = 'I'
        WHERE doctor_id = %s;
        """

        valores = (
            doctor_id
        )
        
        cursor.execute(consulta, valores)  # Ejecutar consulta SQL
        db.commit()  # Confirmar la transacción

        cursor.close()
        db.close()
        return {"success": True, "message": "Asingacines de consultorio inactivadas correctamente"}

    except Exception as e:
        return {"success": False, "error": str(e)}










# def editar_dueno(dueno_id, nombres, apellidos, ci, telf, direccion):
#     """ Edita los datos de un dueño usando el procedimiento almacenado `editar_dueno` """
#     try:
#         db = get_db_connection()
#         cursor = db.cursor()

#         print("Datos enviados a MySQL:", dueno_id, nombres, apellidos, ci, telf, direccion)  # Para depuración

#         cursor.callproc("editar_dueno", (dueno_id, nombres or "", apellidos or "", ci or "", telf or "", direccion or ""))

#         db.commit()
#         cursor.close()
#         db.close()

#         return {"success": True, "message": "Datos del dueño actualizados correctamente"}

#     except Exception as e:
#         return {"success": False, "error": str(e)}

# def descartar_dueno(dueno_id):
#     """ Llama al procedimiento almacenado `descartar_persona` para marcar un dueño como descartado. """
#     try:
#         db = get_db_connection()
#         cursor = db.cursor()

#         print(f"Descartando dueño con ID: {dueno_id}")  # Para depuración

#         cursor.callproc("descartar_persona", (dueno_id,))
#         db.commit()

#         cursor.close()
#         db.close()

#         return {"success": True, "message": "Dueño descartado correctamente"}

#     except Exception as e:
#         return {"success": False, "error": str(e)}

# def obtener_id_dueno(dueno_nombre=None):
#     try:
#         db = get_db_connection()
#         cursor = db.cursor(dictionary=True)
        
#         # Si se pasa un nombre, buscarlo, sino obtener todos los dueños
#         if dueno_nombre:
#             cursor.execute("""
#                 SELECT id 
#                 FROM persona 
#                 WHERE nombres = %s 
#                 AND persona_tipo_id = (SELECT id FROM persona_tipo_id WHERE descripcion = 'Dueño')
#             """, (dueno_nombre,))
#         else:
#             cursor.execute("""
#                 SELECT id, nombres 
#                 FROM persona 
#                 WHERE persona_tipo_id = (SELECT id FROM persona_tipo_id WHERE descripcion = 'Dueño')
#             """)  # Obtener solo los dueños
        
#         resultado = cursor.fetchall() if not dueno_nombre else cursor.fetchone()
#         cursor.close()
#         db.close()
        
#         # Si se pide un dueño específico, devuelve el ID
#         if dueno_nombre:
#             return resultado['id'] if resultado else None
#         # Si no, devuelve una lista de dueños
#         return resultado if resultado else []
#     except Exception as e:
#         print(f"Error al obtener el dueño: {e}")
#         return None

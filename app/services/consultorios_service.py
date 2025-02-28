from config.db import get_db_connection

def obtener_consultorios():
    """ Obtiene la lista de consultorios desde la base de datos """
    try:
        db = get_db_connection()
        cursor = db.cursor()
        consulta = '''
            SELECT 
                c.id,
                c.nro_consultorio,
                GROUP_CONCAT(e.descripcion SEPARATOR ', ') AS equipamientos,
                c.fecha_registro,
                c.estado
            FROM consultorio c
            LEFT JOIN consultorio_equipamiento ce ON c.id = ce.consultorio_id AND ce.estado = 'A'
            LEFT JOIN equipamiento e ON ce.equipamiento_id = e.id
            GROUP BY c.id, c.nro_consultorio, c.fecha_registro, c.estado
            ORDER BY c.nro_consultorio ASC;
        '''
        cursor.execute(consulta)  # Ejecutar consulta SQL
         # Obtener nombres de columnas de manera dinámica
        columnas = [desc[0] for desc in cursor.description]
        # Obtener resultados y construir lista de diccionarios
        consultorios = []
        for row in cursor.fetchall():
            consultorios.append(dict(zip(columnas, row)))  # Empareja cada columna con su valor en la fila
        cursor.close()
        db.close()
        return consultorios

    except Exception as e:
        print(f"Error al obtener doctores: {str(e)}")
        return []
    
# agregar datos a la tabla consultorio
def registrar_consultorio(data):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        # Verificar si el número de consultorio ya existe
        consulta_verificacion = '''
            SELECT COUNT(*) FROM consultorio WHERE nro_consultorio = %s
        '''
        cursor.execute(consulta_verificacion, (data['f_nro_consultorio'],))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            cursor.close()
            db.close()
            return {"success": False, "message": "El número de consultorio ya existe."}

        # Insertar si no existe
        consulta_insert = '''
            INSERT INTO consultorio (nro_consultorio, fecha_registro, estado)
            VALUES (%s, %s, %s)
        '''
        valores = (
            data['f_nro_consultorio'],
            data['f_fecha_registro'],
            data['f_estado'],
        )
        cursor.execute(consulta_insert, valores)
        db.commit()

        cursor.close()
        db.close()
        return {"success": True, "message": "Consultorio registrado correctamente"}
        
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
    

def editar_consultorio(data):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        # Verificar si el número de consultorio ya existe
        consulta_verificacion = '''
            SELECT COUNT(*) FROM consultorio WHERE nro_consultorio = %s
        '''
        cursor.execute(consulta_verificacion, (data['f_nro_consultorio'],))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            cursor.close()
            db.close()
            return {"success": False, "message": "El número de consultorio ya existe."}

        # Insertar si no existe
        consulta_insert = '''
            INSERT INTO consultorio (nro_consultorio, fecha_registro, estado)
            VALUES (%s, %s, %s)
        '''
        valores = (
            data['f_nro_consultorio'],
            data['f_fecha_registro'],
            data['f_estado'],
        )
        cursor.execute(consulta_insert, valores)
        db.commit()

        cursor.close()
        db.close()
        return {"success": True, "message": "Consultorio registrado correctamente"}
        
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}
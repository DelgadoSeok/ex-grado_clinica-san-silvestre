from config.db import get_db_connection
from datetime import datetime

def ver_egresos(fecha_inicio=None, fecha_fin=None):
    """ Obtiene la lista de dueños desde el procedimiento almacenado `ver_dueno` """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.callproc("ver_egresos", (fecha_inicio, fecha_fin))

        # Obtener resultados
        egresos = []
        for result in cursor.stored_results():
            for row in result.fetchall():

                egresos.append({
                    "id": row[0],
                    "observacion": row[1],
                    "monto": row[2],
                    "fecha": row[3],
                    "egreso_tipo_id": row[4],
                    "descartado": row[5]
                })
        
        cursor.close()
        db.close()
        return egresos
    
    except Exception as e:
        print(f"Error al obtener egresos: {str(e)}")
        return []

def crear_egreso(observacion, monto, fecha, egreso_tipo_id):
    """ Registra un nuevo egreso usando el procedimiento almacenado `crear_egreso` """
    print(observacion)
    print(monto)
    print(fecha)
    print(egreso_tipo_id)
    try:
        db = get_db_connection()
        cursor = db.cursor()

        

        cursor.callproc("crear_egreso", (observacion, monto, fecha, egreso_tipo_id))
        db.commit()

        cursor.close()
        db.close()
        return {"success": True, "message": "Egreso registrado correctamente"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

def ver_tipos_egreso():
    """ Obtiene la lista de tipos de egreso desde el procedimiento almacenado `ver_tipos_egreso` """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.callproc("ver_tipos_egreso")
        
        tipos_egreso = []
        for result in cursor.stored_results():
            for row in result.fetchall():
                tipos_egreso.append({
                    "id": row[0],
                    "descripcion": row[1]
                })
        
        cursor.close()
        db.close()
        return tipos_egreso
    
    except Exception as e:
        print(f"Error al obtener tipos de egreso: {str(e)}")
        return []

def editar_egreso(id, observacion, monto, fecha, egreso_tipo_id, descartado=None):
    """ Edita un egreso existente usando el procedimiento almacenado `editar_egreso` """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.callproc("editar_egreso", (id, observacion, monto, fecha, egreso_tipo_id, descartado))
        db.commit()

        cursor.close()
        db.close()
        return {"success": True, "message": "Egreso actualizado correctamente"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

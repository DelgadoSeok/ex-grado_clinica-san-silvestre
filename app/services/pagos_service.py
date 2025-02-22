from config.db import get_db_connection
from datetime import datetime

def reporte_pagos(deuda_id):
    """ Llama al procedimiento almacenado `ver_deudas` para obtener las deudas """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Llamar al procedimiento almacenado
        cursor.callproc("reporte_pago", (deuda_id,))
         # Iterar sobre los resultados devueltos por el procedimiento almacenado
        for result in cursor.stored_results():
            deudas = result.fetchall()

        cursor.close()
        db.close()

        print(deudas)
        return deudas

    except Exception as e:
        print(f"Error al obtener deudas: {str(e)}")
        return []



def crear_deuda(fecha, monto):
    """ Llama al procedimiento almacenado `registrar_pago` para registrar un nuevo pago """
    try:
        # print(f"Registrando pago: Puesto ID: {puesto_id}, Fecha: {fecha}, Monto: {monto}, Interés: {monto_interes}, Deuda ID: {deuda_id}")

        db = get_db_connection()
        cursor = db.cursor()

        # Llamar al procedimiento almacenado con los 5 parámetros
        cursor.callproc("crear_deuda", (fecha, monto))

        db.commit()
        cursor.close()
        db.close()

        return {"success": True, "message": "Deudas para cada puesto creadas correctamente"}
    
    except Exception as e:
        print(f"Error al crear deudas: {str(e)}")
        return {"success": False, "error": str(e)}


# obtiene datos de la tabla deudas de la db y la retorna hacia pagos_route.py
def obtener_deudas():
    """ Llama al procedimiento almacenado `ver_deudas` para obtener las deudas """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Llamar al procedimiento almacenado
        cursor.callproc("ver_deudas")
         # Iterar sobre los resultados devueltos por el procedimiento almacenado
        for result in cursor.stored_results():
            deudas = result.fetchall()

        cursor.close()
        db.close()

        return deudas

    except Exception as e:
        print(f"Error al obtener deudas: {str(e)}")
        return []



def registrar_nuevo_pago(fecha, monto, monto_interes, deuda_id):
    """ Llama al procedimiento almacenado `registrar_pago` para registrar un nuevo pago """
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Llamar al procedimiento almacenado con los 5 parámetros
        cursor.callproc("registrar_pago", (fecha, monto, monto_interes, deuda_id))

        db.commit()
        cursor.close()
        db.close()

        return {"success": True, "message": "Pago registrado correctamente"}
    
    except Exception as e:
        print(f"Error al registrar pago: {str(e)}")
        return {"success": False, "error": str(e)}


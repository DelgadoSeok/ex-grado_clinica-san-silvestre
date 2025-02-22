from config.db import get_db_connection

def verificar_credenciales(usuario, contrasena):
    """ Verifica si el usuario existe y obtiene su rol """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # llmar al procedimiento almacenado
    query = "CALL obtener_rol_usuario(%s, %s)"
    
    cursor.execute(query, (usuario, contrasena))
    usuario_db = cursor.fetchone()

    cursor.close()
    conn.close()

    return usuario_db  # Retorna None si no existe, o los datos del usuario si es válido

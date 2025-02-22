import mysql.connector

#  obtiene la conexión a la db
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mutualista"
    )


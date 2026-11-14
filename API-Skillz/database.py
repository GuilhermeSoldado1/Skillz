import mysql.connector

def get_connection():

    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="libskilliana_guilhermesoldado_n24"
    )

    return conexao


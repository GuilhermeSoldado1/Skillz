import mysql.connector


def get_connection():

    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="minha_base_dados"
    )

    return conexao
import mysql.connector

def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",             
        password="123456",     
        database="respuestos_quibdo_corregido",
        port=3306                
    )
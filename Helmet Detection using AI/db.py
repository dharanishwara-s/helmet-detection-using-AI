import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mottu@123",   
        database="helmet_ai"
    )

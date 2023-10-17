from fastapi import Depends

import mysql.connector
from settings import MySQL_ip
from settings import MySQL_user
from settings import MySQL_password

def get_db_connection():
    connection = mysql.connector.connect(
        host=MySQL_ip,
        port=3306,
        user=MySQL_user,
        password=MySQL_password,
        database="grandet"
    )
    return connection

def get_db():
    connection = get_db_connection()
    db = connection.cursor()

    try:
        yield db
    finally:
        db.close()
        connection.close()

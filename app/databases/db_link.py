from fastapi import Depends

import mysql.connector
from settings import MySQL_ip
from settings import MySQL_port
from settings import MySQL_user
from settings import MySQL_password
from settings import DB_name

def get_db_connection():
    connection = mysql.connector.connect(
        host=MySQL_ip,
        port=MySQL_port,
        user=MySQL_user,
        password=MySQL_password,
        database=DB_name
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

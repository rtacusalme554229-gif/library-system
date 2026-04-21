import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            connection_timeout=5
        )
        return connection

    except Error as e:
        print("Database connection error:", e)
        return None
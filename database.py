import mysql.connector
from mysql.connector import Error
def create_connection():
    try:
        connection=mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='bank_management')
        if connection.is_connected():
            print('Database connected successfulllY')
            return connection
    except Error as e:
        print('Datatabase connection error:',e)
    return None

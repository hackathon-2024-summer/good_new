from sqlalchemy import create_engine, text
import pymysql
import os

host = os.getenv("MYSQL_HOST_FAST")
port = int(os.getenv("PORT_MYSQL_FAST"))
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
db = os.getenv("MYSQL_DB_FAST")

try:
    connection = pymysql.connect(host=host, user=user, password=password, port=port)
    cursor = connection.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db};")
    print(f"Database {db} has been created or already exists.")

    cursor.close()
    connection.close()
    print("MySQL is up")
except Exception as e:
    print("MySQL is not up. Error:", str(e))
    exit(1)

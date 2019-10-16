import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS DHT_data")
        c.execute("CREATE TABLE DHT_data(timestamp DATETIME, temp NUMERIC, hum NUMERIC)")
    except Error as e:
        print(e)

def main():
    database = r"/home/pi/Desktop/Projekt/sqlite/db/baza.db"
    conn = create_connection(database)
    if conn is not None:
        create_table(conn)
    else:
        print("Error, cannot create connection")

if __name__ == '__main__':
    main()
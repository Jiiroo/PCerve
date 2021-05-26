import sqlite3

def conn_db(filename):
    try:
        conn = sqlite3.connect(filename)
    except Error as e:
        pass
        # print(e)
    return conn

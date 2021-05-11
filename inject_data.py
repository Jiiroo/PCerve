import sqlite3


def inject_db(dbname):
    #text = 'assets/{}.db'.format(dbname)
    conn = sqlite3.connect('store_direct.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS details(id integer unique primary key autoincrement, store_name, '
                   'directory)')
    cursor.execute('INSERT INTO details(store_name, directory) VALUES (?,?)',
                    ('PC Express - Bacoor', 'assets/1'))
    conn.commit()
    cursor.close()


n = input('File name:')
inject_db(n)

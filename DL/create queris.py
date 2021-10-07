import sqlite3
from sqlite3 import Error

base_string = '''INSERT INTO addresses (name, url, id)
VALUES ('{}', '{}', {});'''


def export_inserts_file():
    links = []
    try:
        with open(r'heb_pages_links.txt', 'r', encoding="utf-8") as f:
            for line in f:
                li = line.split()
                url = li[0]
                name = ' '.join(li[1:])
                links.append((name, url))
            f.close()
    except Exception as e:
        print(e)
        print('database file did not read', e)
    try:
        with open('pages.txt', 'w', encoding="utf-8") as f:
            id = 0
            for i in links:
                f.write(base_string.format(i[0], i[1], id))
                f.write('\n\n')
                id += 1
            f.close()
    except Exception as e:
        print("error on writing to file")


def create_new_db(name='pagesDB'):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(name)
        conn.executescript('''CREATE TABLE IF NOT EXISTS addresses (
	                            name text UNIQUE ,
	                            url text NOT NULL,
	                            id integer PRIMARY KEY
                                );''')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


create_new_db()

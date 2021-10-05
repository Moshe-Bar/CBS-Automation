import sqlite3
from sqlite3 import Error

#corupted pages
def create_new_db(name='pagesDB'):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(name)
        conn.executescript('''CREATE TABLE IF NOT EXISTS CORRUPTED_PAGES (
	                            last_update date not null,
	                            id integer PRIMARY KEY
                                );''')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

create_new_db()
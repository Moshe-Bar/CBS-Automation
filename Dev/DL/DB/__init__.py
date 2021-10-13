import sqlite3


class DB:
    def __init__(self):
        self.__db = sqlite3.connect(r'D:\Current\Selenium\NewAutomationEnv\Dev\DL\pagesDB')
        self.__cursor = self.__db.cursor()

    def get_he_links(self):
        self.__cursor.execute("SELECT * FROM addresses")
        data = self.__cursor.fetchall()
        return data

    def save_test_result(self, test_key, test_data):
        self.__cursor.executescript('''CREATE TABLE IF NOT EXISTS  {}(
	                            name text UNIQUE ,
	                            url text NOT NULL,
	                            id integer PRIMARY KEY
                                );'''.format(test_key))

    def load_test_data(self, test_key):
        pass




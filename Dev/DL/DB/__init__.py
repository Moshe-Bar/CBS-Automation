import sqlite3


class DB:
    def __init__(self):
        self.__db = sqlite3.connect(r'pagesDB')
        self.__cursor = self.__db.cursor()

    def get_he_links(self):
        self.__cursor.execute("SELECT * FROM addresses")
        data = self.__cursor.fetchall()
        return data

    # def save_test_result(self, test_key, test_data):
    #     inserts=["INSERT INTO TEST_RSLT VALUES ({},{},{},{},{});"]
    #     self.__cursor.executescript('''CREATE TABLE IF NOT EXISTS  {}(
	#                             name text UNIQUE ,
	#                             url text NOT NULL,
	#                             id integer PRIMARY KEY
    #                             );'''.format(test_key))

    def load_test_data(self, test_key):
        pass

    def load_error_details(self):
        self.__cursor.execute("SELECT * FROM ERRORS")
        data = self.__cursor.fetchall()
        return data


x = DB()
print(x.load_error_details())



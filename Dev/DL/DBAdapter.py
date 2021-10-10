import sqlite3

class DBAdapter:
    def __init__(self, db_name='pagesDB'):
        self.__db = sqlite3.connect(r'D:\Current\Selenium\NewAutomationEnv\Dev\DL\pagesDB')
        self.cursor = self.__db.cursor()

    def get_CBS_he_links(self):
        self.cursor.execute("SELECT * FROM addresses")
        data = self.cursor.fetchall()
        return data
        # return [CbsLink(url=i[1],page_name=i[0]) for i in data]

    def save_corrupted_pages(self, pages:[]):
        try:
            #TODO multi inserts for ids
            self.cursor.execute("INSERT ")
            self.cursor.fetchall()
        except Exception as e:
            print('exception in save_corrupted_pages func: ',e)

    def save_test_result(self, test_key, page_id):
        self.cursor.executescript('''CREATE TABLE IF NOT EXISTS  {}(
	                            name text UNIQUE ,
	                            url text NOT NULL,
	                            id integer PRIMARY KEY
                                );'''.format(test_key))

    # def __del__(self):
    #     self.cursor.close()

# x=DBAdapter()
# print(x.get_CBS_he_links())
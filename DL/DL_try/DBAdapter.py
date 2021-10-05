import sqlite3

from CbsObjects.CbsLink import CbsLink


class DBAdapter:
    def __init__(self, db_name='pagesDB'):
        self.__db = sqlite3.connect(db_name)
        self.cursor = self.__db.cursor()

    def get_CBS_he_links(self):
        self.cursor.execute("SELECT * FROM addresses")
        data = self.cursor.fetchall()
        return data
        # return [CbsLink(url=i[1],page_name=i[0]) for i in data]

    def save_corrupted_pages(self, page_id:[]):
        try:
            self.cursor.execute("INSERT ")
            self.cursor.fetchall()
        except Exception as e:
            print('exception in save_corrupted_pages func: ',e)

    def __del__(self):
        self.__db.close()


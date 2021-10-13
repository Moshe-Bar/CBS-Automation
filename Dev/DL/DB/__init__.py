import sqlite3



class DB:
    def __init__(self):
        self.__db = sqlite3.connect(r'D:\Current\Selenium\NewAutomationEnv\Dev\DL\pagesDB')
        self.__cursor = self.__db.cursor()


    def get_CBS_he_links(self):
        self.__cursor.execute("SELECT * FROM addresses")
        data = self.__cursor.fetchall()
        return data


    # def save_corrupted_pages(self, pages: []):
    #     try:
    #         # TODO multi inserts for ids
    #         self.__cursor.execute("INSERT ")
    #         self.__cursor.fetchall()
    #     except Exception as e:
    #         print('exception in save_corrupted_pages func: ', e)

    def save_test_result(self, test_key, page_id):
        self.__cursor.executescript('''CREATE TABLE IF NOT EXISTS  {}(
	                            name text UNIQUE ,
	                            url text NOT NULL,
	                            id integer PRIMARY KEY
                                );'''.format(test_key))


    def get_xpath(self, xp_object):
        # return self.__xpath[xp_object]
        return self.__xpath[xp_object]

    def get_webdriver_path(self):
        return self.__web_driver['driver_path']


x = DB()
print(x.get_xpath("MAP_LINKS_XPATH"))
print(x.get_webdriver_path())

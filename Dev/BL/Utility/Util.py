from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from Objects.Page import SubjectPage
from Dev.DL import Adapter

class TestResult:
    def __init__(self,scanned_page):
        self.page:SubjectPage = scanned_page
        self.db_rows = self.to_rows()

    def __repr__(self):

    def to_rows(self):
        for i in len(self.page.)#TODO add to page repr func

class Util:
    def __init__(self):
        self.__db = Adapter()

    # returns array of SubjectPages
    def get_pages(self, lang='he'):
        raw_pages = self.__db.get_he_links()
        return [SubjectPage(pageName=p[0], pageLink=p[1], pageID=p[2]) for p in raw_pages]

    # returns a web driver with options
    def get_web_driver(self, wait_time=2, withUI=True):
        driver_path = self.__db.get_driver_path()
        try:
            if not withUI:
                options = webdriver.ChromeOptions()
                options.add_argument("headless")
                # options.add_argument('--disable-gpu')
                driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)

            else:
                driver = webdriver.Chrome(executable_path=driver_path)


            driver.implicitly_wait(wait_time)
            return driver

        except WebDriverException as e:
            print("couldn't create driver: ", e)
            return None

    # load data of test by key
    def load_test_data(self, test_key):
        # TODO
        pass

    # save the test data and returns the kei for it
    def save_test_data(self,data):
        # TODO
        pass







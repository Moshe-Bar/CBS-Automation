from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from CbsObjects.Page import SubjectPage
from Dev.DL.DB import DB


class Util:
    def __init__(self):
        self.__db = DB()

    # returns array of SubjectPages
    def get_pages(self, lang='he'):
        raw_pages = self.__db.get_CBS_he_links()
        return [SubjectPage(pageName=p[0], pageLink=p[1], pageID=p[2]) for p in raw_pages]

    # returns a web driver with options
    def get_web_driver(self, wait_time=2, withUI=True):
        driver_path = self.__db.get_webdriver_path()
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



x = Util()
print('len: ', len(x.get_pages()), 'first: ', x.get_pages()[1])

import os
import sys
import chromedriver_autoinstaller

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from win32com.client import Dispatch

from DataBase.DataBase import Links

ROOT = sys.path[1]


class Util:
    @classmethod
    def create_web_driver(cls, withUI=True):
        cls.__init_browser_driver()

        driver_service = Service(Links.CHROME_DRIVER.value)
        options = webdriver.ChromeOptions()
        driver = None
        if not withUI:
            options.headless(True)
        try:
            driver = webdriver.Chrome(service=driver_service, chrome_options=options)
        except WebDriverException as e:
            print('session not created')
            raise e

        return driver

    @classmethod
    def __check_chrome_version(cls):
        return chromedriver_autoinstaller.get_chrome_version()
        # paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        #          r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
        # path = list(filter(lambda x: os.path.isfile(x), paths))[0]
        # parser = Dispatch("Scripting.FileSystemObject")
        # try:
        #     version = parser.GetFileVersion(path)
        #     version = version.split('.')[0]
        # except Exception:
        #     print('chrome version is unknown')
        #     return None
        # return version

    @classmethod
    def __init_browser_driver(cls):
        chromedriver_autoinstaller.install(path=ROOT + '\\Resources\\WebDrivers')




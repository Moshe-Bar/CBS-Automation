from multiprocessing import Process
from queue import Queue
from Util import Util
from selenium import webdriver

from Utility.TestUtility import TestUtility


class AutoTest:
    def __init__(self,candidates:set,visible=True):
        # presences
        self.__candidates = candidates
        self.__scanned = None
        self.__start_date_time = None
        self.__end_date_time =None
        self.__web_driver:webdriver.Chrome = Util.create_web_driver(visible)
        self.__data_share = {'data': Queue(), 'progress': Queue(), 'end_flag': Queue(),'intra':Queue()}
        self.__test_process = Process(target=TestUtility.test, args=(*self.__data_share.values(), self.__candidates, True))

    def pipes(self):
        return self.__data_share

    def start(self):
        pass

    def __end(self):
        try:
            self.__web_driver.close()
            self.__test_process.terminate()
            self.__test_process.join()
        except Exception as e:
            print('Exception in __end func in AutoTest object')

    def __del__(self):
         self.__end()


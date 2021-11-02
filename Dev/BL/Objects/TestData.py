# from Objects.Page import SubjectPage
import datetime
from enum import Enum




class TestData:
    def __init__(self,start_time):
        self.__num_pages = 0
        self.__pages = []
        self.__start_date = start_time
        self.__end_date = None

    def add_page(self, page):
        self.__pages.append(page)
        self.__num_pages += 1

    def get_pages(self):
        return self.__pages

    def __repr__(self):
        self.__end_date = datetime.datetime.now()

print(datetime.datetime.now())
print(datetime.datetime.now(datetime.timezone.))
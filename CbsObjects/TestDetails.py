import time
import uuid


class TestDetails:
    def __init__(self,candidates):
        self.__id = uuid.uuid4()
        self.__candidate_pages = candidates
        self.__scanned_pages=set()
        self.__start_time = ''
        self.__end_time = ''

    def add_scanned_page(self,page_id):
        self.__scanned_pages.add(page_id)

    def start(self):
        if self.__start_time is None:
            self.__start_time=time.strftime('%d/%m/%Y_%H:%M:%S')

    def end(self):
        if self.__end_time is None:
            self.__end_time = time.strftime('%d/%m/%Y_%H:%M:%S')

    def to_row(self):
        return self.__id,self.__start_time,self.__end_time,self.__candidate_pages,self.__scanned_pages
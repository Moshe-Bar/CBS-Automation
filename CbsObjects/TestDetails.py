import time
import uuid


class TestDetails:
    def __init__(self,candidates:list):
        self.__id = str(uuid.uuid4())
        self.__candidate_pages = candidates
        self.__scanned_pages=[]
        self.__start_date = None
        self.__start_time = None
        self.__end_date = None
        self.__end_time = None

    def add_scanned_page(self,page_id):
        self.__scanned_pages.append(page_id)

    def started(self):
        if self.__start_date is None:
            self.__start_date=time.strftime('%d/%m/%Y')
            self.__start_time=time.strftime('%H:%M:%S')

    def ended(self):
        if self.__end_date is None:
            self.__end_date = time.strftime('%d/%m/%Y')
            self.__end_time = time.strftime('%H:%M:%S')

    def to_list(self):
        return (self.__id, self.__start_time, self.__end_time, str(self.__candidate_pages), str(self.__scanned_pages))

    def start_date(self):
        self.started()
        return self.__start_date, self.__start_time

    def end_date(self):
        self.ended()
        return self.__end_date, self.__end_time

    def candidates(self):
        return self.__candidate_pages

    def key(self):
        return self.__id
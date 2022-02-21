import time
import uuid

class TestDetails:
    def __init__(self, candidates: list):
        self.__id = str(uuid.uuid4())
        it = iter(candidates)
        self.__candidate_pages = dict(zip(it,range(len(candidates))))
        self.__scanned_pages = dict()
        self.__start_date = None
        self.__start_time = None
        self.__end_date = None
        self.__end_time = None

    def add_scanned_page(self, page_id):
        if not self.__candidate_pages.get(page_id) is None:
            self.__scanned_pages.update({page_id:self.__candidate_pages.pop(page_id)})
        else:
            raise Exception('Can not insert tested page ,the page is not exist in candidates for test')

    def started(self):
        if not self.__start_date is None:
            raise Exception('can not start more than one time')
        self.__start_date = time.strftime('%d/%m/%Y')
        self.__start_time = time.strftime('%H:%M:%S')

    def ended(self):
        if not self.__end_date is None:
            raise Exception('can not end more than one time')
        self.__end_date = time.strftime('%d/%m/%Y')
        self.__end_time = time.strftime('%H:%M:%S')

    def to_list(self):
        return self.__id, self.__start_date, self.__start_time,self.__end_date, self.__end_time, str(self.__candidate_pages), str(self.__scanned_pages)

    def start_date_str(self):
        if not self.__start_date:
            raise Exception('start date was not initialized')
        return self.__start_date + ' ' + self.__start_time

    def end_date_str(self):
        if not self.__start_date:
            raise Exception('end date was not initialized')
        return self.__end_date + ' ' + self.__end_time

    def start_date(self):
        if not self.__start_date:
            raise Exception('start date was not initialized')
        return self.__start_date, self.__start_time

    def end_date(self):
        if not self.__start_date:
            raise Exception('end date was not initialized')
        return self.__end_date, self.__end_time

    def candidates(self):
        return self.__candidate_pages

    def key(self):
        return self.__id

    def scanned(self):
        return self.__scanned_pages

    def ID(self):
        return self.__id



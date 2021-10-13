from Objects.Page import SubjectPage


class TestData:
    def __init__(self):
        self.__num_pages = 0
        self.__pages = []
        self.__start_date = None
        self.__end_date = None

    def add_page(self, page: SubjectPage):
        self.__pages.append(page)
        self.__num_pages += 1

    def get_pages(self):
        return self.__pages

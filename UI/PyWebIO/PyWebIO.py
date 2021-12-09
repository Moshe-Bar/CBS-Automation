import json
from multiprocessing import Queue
import threading

from pywebio.input import input, FLOAT, CHECKBOX, input_group, NUMBER, actions, TEXT, PASSWORD, select, checkbox, SELECT
from pywebio.output import put_text, put_code, put_processbar, put_link

from Utility.TestUtility import TestUtility


class WebTest:
    def __init__(self):
        self.pages_list = TestUtility.get_he_pages()
        self.data_share = (Queue(), Queue(), Queue())

        self.chosen_pages = self.choose_pages()
        self.start_test()

    def create_ui(self):
        self.progress_bar = put_processbar('bar')

    def choose_pages(self):
        pages = list(map(lambda page: {'label': page.name, 'value': page.id, "selected": True}, self.pages_list))
        chosen_pages = checkbox('Choose pages to test:', options=pages)
        return list(filter(lambda x: x.id in chosen_pages, self.pages_list))

    def start_test(self):
        self.test_thread = threading.Thread(target=TestUtility.test, args=self.data_share)
        self.observer_thread = threading.Thread(target=self.observe_test, args=(*self.data_share, self.test_thread))

        self.test_thread.start()
        self.observer_thread.start()
        self.observer_thread.join()
        self.test_thread.join()

    def update_client_data(self,data:tuple):
        if data[0] == 'text':
            put_text(data[1])
        elif data[0] == 'link':
            put_link(name=data[1], url=data[2],new_window=True)


    def update_client_bar(self,data):
        pass


    def observe_test(self,data: Queue, progress: Queue, end_flag: Queue, test_thread: threading.Thread):
        while test_thread.is_alive() and end_flag.empty():
            if not data.empty():
                self.update_client_data(data.get())

            if not progress.empty():
                self.update_client_bar(progress.get())

        if not data.empty():
            put_text(data.get())
        if not progress.empty():
            put_text(progress.get())
        print('leaving observer')





if __name__ == '__main__':
    test = WebTest()

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


    def create_ui(self):
        self.progress_bar = put_processbar('bar')

    def choose_pages(self):

        pages = list(map(lambda page: {'label': page.name, 'value': page.id, "selected": True}, pages_list))
        chosen_pages = checkbox('Choose pages to test:', options=pages)
        return list(filter(lambda x: x.id in chosen_pages, pages_list))

    def start_test(self):
        self.test_thread = threading.Thread(target=TestUtility.test, args=self.data_share)
        self.observer_thread = threading.Thread(target=self.observe_test, args=(*self.data_share, self.test_thread))

        self.test_thread.start()
        self.observer_thread.start()
        self.observer_thread.join()
        self.test_thread.join()

    def update_client_data(data: tuple):
        if data[0] == 'text':
            put_text(data[1])
        elif data[0] == 'link':
            put_link(name=data[1], url=data[2])


    def update_client_bar(data):
        pass


    def observe_test(data: Queue, progress: Queue, end_flag: Queue, test_thread: threading.Thread):
        while test_thread.is_alive() and end_flag.empty():
            if not data.empty():
                update_client_data(data.get())

            if not progress.empty():
                update_client_bar(progress.get())

        if not data.empty():
            put_text(data.get())
        if not progress.empty():
            put_text(progress.get())
        print('leaving observer')


# def main():
#     pages_for_test = choose_pages()
#     shared_data = Queue()
#     progress = Queue()
#     end_flag = Queue()
#     test_thread = threading.Thread(target=TestUtility.test,args=(shared_data,progress,end_flag,pages_for_test))
#     observer_thread = threading.Thread(target=observe_test,args=(shared_data,progress,end_flag,test_thread))
#     test_thread.start()
#     observer_thread.start()
#     observer_thread.join()
#     test_thread.join()
#     print('leaving main')


# if __name__ == '__main__':
#     main()

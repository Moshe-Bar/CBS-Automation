import json
from multiprocessing import Queue, Process
import threading

import pywebio
from pywebio import start_server
from pywebio.input import input, FLOAT, CHECKBOX, input_group, NUMBER, actions, TEXT, PASSWORD, select, checkbox, SELECT
from pywebio.output import put_text, put_code, put_processbar, put_link, put_scrollable, put_scope, OutputPosition, \
    set_processbar, use_scope
from pywebio.pin import put_checkbox
from pywebio.session import register_thread

from Utility.TestUtility import TestUtility


class WebTest:
    def __init__(self):
        self.pages_list = TestUtility.get_he_pages()
        self.data_share = (Queue(), Queue(), Queue())
        self.chosen_pages = None

    def set_test_progress(self):
        put_scrollable(put_scope('test_results'), height=350, keep_bottom=True, position=OutputPosition.BOTTOM)
        put_processbar('bar').style("height='50px'")

    def choose_pages(self):
        pages = list(map(lambda page: {'label': page.name, 'value': page.id, "selected": True}, self.pages_list))

        put_scrollable(put_scope('pages'))
        # height=350)
        with use_scope('pages'):
            chosen_pages = checkbox(name='ch', options=pages)
            # chosen_pages = put_checkbox(name='ch', options=pages)
        # chosen_pages = put_checkbox(name='pages_checkbox',label='Choose pages to test:', options=pages,scope='pages')
            self.chosen_pages = list(filter(lambda x: x.id in chosen_pages, self.pages_list))

    def start_test(self):
        self.set_test_progress()
        self.test_thread = Process(target=TestUtility.test, args=self.data_share, daemon=True)
        self.observer_thread = threading.Thread(target=self.observe_test, args=(*self.data_share, self.test_thread), daemon=False)
        # pywebio.session.register_thread(self.test_thread)
        pywebio.session.register_thread(self.observer_thread)
        self.test_thread.start()
        self.observer_thread.start()
        self.observer_thread.join()
        self.test_thread.join()

    def update_client_data(self, data: tuple):
        if data[0] == 'text':
            put_text(data[1], scope='test_results')
        elif data[0] == 'link':
            if data[3] == 'Fail':
                put_link(name=data[1], url=data[2], new_window=True, scope='test_results').style('color:red')
            elif data[3] == 'Pass':
                put_link(name=data[1], url=data[2], new_window=True, scope='test_results')


    def update_client_bar(self, data):
        set_processbar('bar', data)

    def observe_test(self, data: Queue, progress: Queue, end_flag: Queue, test_thread: threading.Thread):
        while test_thread.is_alive() and end_flag.empty():
            if not data.empty():
                self.update_client_data(data.get())

            if not progress.empty():
                self.update_client_bar(progress.get())

        if not data.empty():
            self.update_client_data(data.get())
        if not progress.empty():
            self.update_client_bar(progress.get())
        print('leaving observer')


def main():
    test = WebTest()
    test.choose_pages()
    test.start_test()


def online():
    return True


if __name__ == '__main__':
    is_cdn  = True if online() else False
    start_server(main, auto_open_webbrowser=True, port=8080, debug=True,cdn=is_cdn)

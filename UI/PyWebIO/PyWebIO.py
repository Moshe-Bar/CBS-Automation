from multiprocessing import Queue, Process
import threading

import pywebio
import urllib3
# from pywebio import start_server
from pywebio.input import checkbox, input_group
from pywebio.output import put_text, put_processbar, put_link, put_scrollable, put_scope, OutputPosition, \
    set_processbar, use_scope
# from pywebio.pin import put_checkbox
# from pywebio.session import register_thread
from pywebio.pin import put_checkbox, put_input

from Utility.TestUtility import TestUtility


class WebTest:
    def __init__(self):
        self.pages_list = TestUtility.get_he_pages()
        self.chosen_pages = None
        self.data_share = (Queue(), Queue(), Queue())

    def set_test_progress(self):
        put_scrollable(put_scope('test_results'), height=350, keep_bottom=True, position=OutputPosition.BOTTOM)
        put_processbar('bar').style("height='50px'")
        put_input('a', type='button', value=0)

    def choose_pages(self):
        pages = list(map(lambda page: {'label': page.name, 'value': page.id, "selected": True}, self.pages_list))
        # put_scrollable(put_scope('pages'))
        # height=350)
        # ig = input_group()
        self.chosen_pages = checkbox(label='Chose_pages', options=pages,
                            other_html_attrs={'style': 'overflow-y: scroll; height:400px;'}
                            )
        # chosen_pages = put_checkbox(name='ch', options=pages)
        # chosen_pages = put_checkbox(name='pages_checkbox',label='Choose pages to test:', options=pages,scope='pages')
        # return list(filter(lambda x: x.id in pages_id, self.pages_list))


    def start_test(self):
        self.set_test_progress()


        # print(data)
        self.test_proc = Process(target=TestUtility.test, args=(*self.data_share,self.chosen_pages,True))
        self.observer_thread = threading.Thread(target=self.observe_test, args=(*self.data_share, self.test_proc))
        # pywebio.session.register_thread(self.test_thread)
        pywebio.session.register_thread(self.observer_thread)

        self.test_proc.start()
        self.observer_thread.start()

        self.observer_thread.join()
        self.test_proc.join()

    def update_client_data(self, data: tuple):
        if data[0] == 'text':
            put_text(data[1], scope='test_results')
        elif data[0] == 'link':
            if data[3] == 'Fail':
                put_link(name=data[1], url=data[2], new_window=True, scope='test_results').style('color:red')
            elif data[3] == 'Pass':
                put_link(name=data[1], url=data[2], new_window=True, scope='test_results')
                put_text('Pass!', scope='test_results')

    def update_client_bar(self, data):
        set_processbar('bar', data)

    def observe_test(self, data: Queue, progress: Queue, end_flag: Queue, test_proc: Process):
        while test_proc.is_alive() and end_flag.empty():
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
    http = urllib3.PoolManager(timeout=3.0)
    try:
        r = http.request('GET', 'https://www.google.com/', preload_content=False)
    except Exception as err:
        print(f'Offline test {err}')
        return False
    code = r.status
    r.release_conn()
    if code == 200:
        print('Online test')
        return True
    else:
        print('Offline test')
        return False


if __name__ == '__main__':
    is_cdn = True if online() else False
    pywebio.start_server(main, auto_open_webbrowser=True, port=8080, cdn=is_cdn)

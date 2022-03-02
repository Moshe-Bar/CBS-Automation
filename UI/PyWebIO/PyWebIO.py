import time
from multiprocessing import Queue, Process
import threading

import pywebio
import urllib3
# from pywebio import start_server
from pywebio.input import checkbox, input_group, actions
from pywebio.output import put_text, put_processbar, put_link, put_scrollable, put_scope, OutputPosition, \
    set_processbar, use_scope, put_html, put_file

from pywebio.pin import put_checkbox, put_input

from Utility.TestUtility import TestUtility


class WebTest:
    def __init__(self):
        self.pages_list = TestUtility.get_he_pages()
        self.chosen_pages = None
        self.data_share = {'data': Queue(), 'progress': Queue(), 'end_flag': Queue()}
        self.test_proc = None
        self.observer_thread = None
        self.test_key = None

    def set_test_progress(self):
        put_scope('global')
        with use_scope('global', clear=True):
            put_scrollable(put_scope(name='test_results'), height=350, keep_bottom=True, position=OutputPosition.BOTTOM)
            put_processbar('bar').style("height='50px'")

        # while True:
        self.start_button = {
            "label": 'Start',
            "value": 'Start test',
            "disabled": False
        }
        self.stop_button = {
            "label": 'Stop',
            "value": 'Stop test',
            "disabled": True,
            "color": 'danger'
        }
        self.results_button = {
            "label": 'Results',
            "value": 'Test Results',
            "disabled": True,
        }
        while True:
            req = input_group('Test control buttons', [
                actions(name='cmd', buttons=[self.start_button, self.stop_button, self.results_button])],
                              validate=lambda input: ('msg', 'Message content cannot be empty') if input[
                                                                                                       'cmd'] == 'Stop' and not
                                                                                                   input[
                                                                                                       'msg'] else None)
            # ],
            if req['cmd'] == 'Start test':
                print('start clicked')
                self.start_button.update({"disabled": True})
                self.stop_button.update({"disabled": False})
                self.start_test()
            elif req['cmd'] == 'Stop test':
                print('stop clicked')
                # self.start_button.update({"disabled": False})
                # self.stop_button.update({"disabled": True})
                # self.results_button.update({"disabled": False})
                self.stop_test()
            elif req['cmd'] == 'Test Results':
                self.get_test_results(self.test_key)
                break

    def choose_pages(self):
        pages = list(map(lambda page: {'label': page.name, 'value': page.id, "selected": True}, self.pages_list))

        self.chosen_pages = checkbox(label='Chose_pages', options=pages,
                                     other_html_attrs={'style': 'overflow-y: scroll; height:400px;'}
                                     )
        self.set_test_progress()

    def start_test(self):
        self.test_proc = Process(target=TestUtility.test, args=(*self.data_share.values(), self.chosen_pages, True))
        self.observer_thread = threading.Thread(target=self.observe_test,
                                                args=(*self.data_share.values(), self.test_proc))

        pywebio.session.register_thread(self.observer_thread)

        self.test_proc.start()
        self.observer_thread.start()

        # self.observer_thread.join()
        # self.test_proc.join()

    def update_client_data(self, data: tuple):
        if data[0] == 'text':
            with use_scope('global'):
                put_text(data[1], scope='test_results')
        elif data[0] == 'link':
            if data[3] == 'Fail':
                with use_scope('global'):
                    put_link(name=data[1], url=data[2], new_window=True, scope='test_results').style('color:red')
            elif data[3] == 'Pass':
                with use_scope('global'):
                    put_link(name=data[1], url=data[2], new_window=True, scope='test_results')
                    put_text('Pass!', scope='test_results')
        elif data[0] == 'key':
            self.test_key = data[1]

    def update_client_bar(self, data):
        set_processbar('bar', data)

    def observe_test(self, data: Queue, progress: Queue, end_flag: Queue, test_proc: Process):
        while test_proc.is_alive() and end_flag.empty():
            if not data.empty():
                self.update_client_data(data.get())

            if not progress.empty():
                self.update_client_bar(progress.get())
        while test_proc.is_alive():
            test_proc.terminate()
            # test_proc.close()
            test_proc.join()

        if not data.empty():
            self.update_client_data(data.get())
        if not progress.empty():
            self.update_client_bar(progress.get())
        self.end_test()
        print('leaving observer')

    def get_test_results(self, key):
        with use_scope('global', clear=True):
            put_scrollable(put_scope(name='test_results'), height=350, keep_bottom=True)
            data = TestUtility.get_test_results_as_html(key)
            put_html(data, scope='test_results')
            put_file(label='results as html', name='results.html', content=data.encode('utf-8'))
            pdf_data = TestUtility.get_test_result_as_pdf(key)
            excel_data = TestUtility.get_test_results_as_excel(key)
            put_file(label='results as pdf', name='results.pdf', content=pdf_data)
            put_file(label='results as excel', name='results.xlsx', content=excel_data)

        # self.go_to_test_results(key='test_results')

    def end_test(self):
        self.start_button.update({"disabled": False})
        self.stop_button.update({"disabled": True})
        self.results_button.update({"disabled": False})

    def stop_test(self):
        self.end_test()
        self.data_share.get('data').put('test was canceled by the user')
        self.data_share.get('end_flag').put('canceled by user')
        while self.test_proc.is_alive():
            self.test_proc.terminate()
            self.test_proc.join()
        self.end_test()
        # self.test_proc.close()
        # time.sleep(1)

    def go_to_test_results(self, key):
        pass


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
#     ,remote_access=True
#     auto_open_webbrowser=True

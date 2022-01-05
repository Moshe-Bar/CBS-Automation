import threading
import time
from multiprocessing import Queue, Process, freeze_support
import tornado

import pywebio
import urllib3.request

from pywebio import start_server
from pywebio.input import checkbox
from pywebio.output import put_text, put_loading, put_processbar, set_processbar, put_markdown, put_file, put_table, \
    put_buttons, put_html, span, put_scrollable, put_scope, put_grid, put_collapse

#################import warnings

# from selenium import webdriver

###########warnings.filterwarnings("error")
from pywebio.pin import put_input

from pywebio.session import register_thread, run_async, run_asyncio_coroutine

from Utility.TestUtility import TestUtility


def offline():
    http = urllib3.PoolManager(timeout=3.0)
    try:
        r = http.request('GET', 'http://216.58.192.142', preload_content=False)
    except Exception as err:
        return False
    code = r.status
    r.release_conn()
    if code == 200:
        return True
    else:
        return False

def f_5(a,b,c,d,e):
    print(a+b+c+d+e)

def main():
    put_scrollable(put_scope('test_results'), height=350, keep_bottom=True)
    put_processbar('bar').style("height='50px'")

    # test_proc = Process(target=TestUtility.test, args=(*data,pages,visible))
    ##test_proc = Process(target=TestUtility.test, args=(*s,))
    # self.observer_thread = threading.Thread(target=self.observe_test, args=(*self.data_share, self.test_proc))
    # pywebio.session.register_thread(self.test_thread)
    # pywebio.session.register_thread(self.observer_thread)

    # observer_thread.start()
    ##test_proc.start()
    # observer_thread.join()
    ##test_proc.join()

    # op = {'label': 'first', 'value': 1, "selected": True}, {'label': 'second', 'value': 2, "selected": True}
    # op = list(op)
    # ch = checkbox(options=op)
    # print(ch)


if  __name__ == '__main__':
    freeze_support()
    main()


# if __name__ == '__main__':
#     cdn = True
#     if offline():
#         cdn = False
#     start_server(applications=main, auto_open_webbrowser=True, port=10012)

    # except RuntimeWarning:
    #     import ipdb
    #
    #     ipdb.set_trace()
    # except RuntimeWarning:
    #     import ipdb
    #     ipdb.set_trace()
    #

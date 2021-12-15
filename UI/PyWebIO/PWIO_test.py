import threading
import time
from multiprocessing import Queue, Process
import tornado

import pywebio
import urllib3.request

from pywebio import start_server
from pywebio.output import put_text, put_loading, put_processbar, set_processbar, put_markdown, put_file, put_table, \
    put_buttons, put_html, span, put_scrollable, put_scope, put_grid, put_collapse

import warnings

# from selenium import webdriver

warnings.filterwarnings("error")

from pywebio.session import register_thread, run_async, run_asyncio_coroutine

from Utility.TestUtility import TestUtility


def timer(q_list):
    # await timer2()
    TestUtility.test(shared_data=q_list[0], progress_status=q_list[1], end_flag=q_list[2])


def timer2(q_list):
    i = 0
    while True:
        time.sleep(2)
        print(i)
        put_text(f'timer2: {i}')
        i += 1


def main():
    q_list = (Queue(), Queue(), Queue())
    # run_asyncio_coroutine(timer(q_list))
    # run_async(timer(q_list))
    # await timer2()
    # run_async(timer2())
    # print('try starting thread..')
    #
    t1 = Process(target=timer, args=(q_list,))

    t2 = threading.Thread(target=timer2)
    t1.start()
    print('thread is running')

    # register_thread(t1)
    register_thread(t2)

    t2.start()
    t1.join()
    t2.join()


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


if __name__ == '__main__':
    cdn = True
    if offline():
        cdn = False
    start_server(applications=main,auto_open_webbrowser=True, port=8080, cdn=False)

    # except RuntimeWarning:
    #     import ipdb
    #
    #     ipdb.set_trace()
    # except RuntimeWarning:
    #     import ipdb
    #     ipdb.set_trace()
    #

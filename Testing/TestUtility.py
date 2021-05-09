import threading
import time
from multiprocessing import Queue

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# # from CbsClasses.CbsPageUtility import CbsPageUtility
# import asyncio
# from concurrent.futures import ThreadPoolExecutor

from CbsClasses.CbsPage import CbsPage
from Testing.CbsPageUtility import CbsPageUtility
from dataBase.DataBase import DataBase, Links


class TestUtility:

    @classmethod
    def test_web_parts(cls, page: CbsPage, open_session: webdriver.chrome, statistical=False):
        pass

    @classmethod
    def get_sessions(cls, amount=1, timeout=10, isViseble=True):
        if amount == 1:
            return cls.create_web_driver(timeout, isViseble)
        sessions = []
        for i in range(amount):
            sessions.append(cls.create_web_driver(timeout, isViseble))
        return sessions

    @classmethod
    def get_pages(cls):
        pages = DataBase.get_CBS_pages()
        return pages

    @classmethod
    def initial_test_environment_(cls, wait_time=10, async_=False, pages=[]):
        if async_:
            sessions = cls.get_sessions(amount=len(pages), timeout=wait_time)
            pages = DataBase.get_CBS_pages()
            # with ThreadPoolExecutor
            for i, session in enumerate(sessions):
                cls.testPage(pages[i], session)
        # TODO

    @classmethod
    def create_web_driver(cls, wait_time=10, withUI=True):
        try:
            if not withUI:
                options = webdriver.ChromeOptions()
                options.add_argument("headless")
                # options.add_argument('--disable-gpu')
                driver = webdriver.Chrome(executable_path=Links.CHROME_DRIVER.value, chrome_options=options)
            else:
                driver = webdriver.Chrome(executable_path=Links.CHROME_DRIVER.value)

            # driver.implicitly_wait(wait_time)
            return driver
        except WebDriverException as e:
            print('driver error: ' + str(e))
            return None

    @classmethod
    def testPage(cls, page: CbsPage, session: webdriver.Chrome):
        CbsPageUtility.set_statistical_part(page, session)

    #     TODO another web part
    #     TODO another web part
    #     TODO another web part
    #     TODO another web part

    # visible func
    @classmethod
    def test(cls, shared_data: Queue = Queue(), progress_status: Queue = Queue(), end_flag: Queue = Queue(),
             pages=None, session_visible=True):

        if pages is None:
            try:
                pages = cls.get_pages()
            except Exception as e:
                print('error in loading pages, test is closed')
                shared_data.put('error in loading pages, test is closed')
                end_flag.put('error in loading pages, test is closed')
                raise e

        # status flow
        shared_data.put('initializing test environment...')
        print('initializing test environment...')
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        shared_data.put('test started on: ' + str(current_time))
        print('test started on: ' + str(current_time))

        try:
            session = cls.get_sessions(isViseble=session_visible)  # default as synchronous test - one instance session
        except Exception as e:
            print('error loading sessions, test is closed')
            shared_data.put('error loading sessions, test is closed')
            end_flag.put('error loading sessions, test is closed')
            raise e

        error_pages = []
        pages_size = len(pages)
        print('num pages', str(len(pages)))
        shared_data.put('num pages: ' + str(pages_size))

        try:
            for i, page in enumerate(pages):
                if end_flag.qsize() > 0:
                    raise Exception('test canceled')
                    # outside canceled
                percents = i / pages_size
                progress_status.put(str("%.1f" % percents) + '%')
                print(str("%.1f" % percents) + '%')

                session.get(page.link.url)
                cls.testPage(page, session)

                if len(page.stats_part.errors) > 0:
                    print(page.name, page.link.url)
                    print(page.stats_part.errors)
                    shared_data.put(str(page.name)[::-1])
                    shared_data.put(page.stats_part.errors)
                    error_pages.append((page.name, page.link.url, page.stats_part.errors))
                else:
                    shared_data.put(str(page.name)[::-1])
                    shared_data.put(str(200))

        except Exception as e:
            print('main process stopped due to exception: ' + str(e))
            shared_data.put('main process stopped due to exception: ' + str(e))
            end_flag.put('main process stopped due to exception: ' + str(e))
        finally:
            session.close()
            end_flag.put('end main process')
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            # str(time.time() - start_time)
            print('test ended on: ' + current_time)
            shared_data.put('test ended on: ' + current_time)

    @classmethod
    def test_with_events(cls, working: threading.Event(), shared_data: Queue = Queue(),
                         progress_status: Queue = Queue(),
                         pages=None):

        if pages is None:
            try:
                pages = cls.get_pages()
            except Exception as e:
                print('error in loading pages, test is closed')
                shared_data.put('error in loading pages, test is closed')
                working.clear()
                raise e

        # status flow
        shared_data.put('initializing test environment...')
        print('initializing test environment...')
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        shared_data.put('test started on: ' + str(current_time))
        print('test started on: ' + str(current_time))

        try:
            session = cls.get_sessions()  # default as synchronous test - one instance session
        except Exception as e:
            print('error loading sessions, test is closed')
            shared_data.put('error loading sessions, test is closed')
            working.clear()
            raise e

        error_pages = []
        pages_size = len(pages)
        print('num pages', str(len(pages)))
        shared_data.put('num pages: ' + str(pages_size))

        try:
            for i, page in enumerate(pages):
                if not working.isSet():
                    raise Exception('test canceled')
                    # outside canceled

                percents = i / pages_size
                progress_status.put(percents)
                print(str("%.1f" % percents) + '%')

                session.get(page.link.url)
                cls.testPage(page, session)

                if len(page.stats_part.errors) > 0:
                    print(page.name, page.link.url)
                    print(page.stats_part.errors)
                    shared_data.put(str(page.name)[::-1])
                    shared_data.put(page.stats_part.errors)
                    error_pages.append((page.name, page.link.url, page.stats_part.errors))
                else:
                    shared_data.put(str(page.name)[::-1])
                    shared_data.put(str(200))

        except Exception as e:
            print('main process stopped due to exception: ' + str(e))
            shared_data.put('main process stopped due to exception: ' + str(e))
            # end_flag.put('main process stopped due to exception: ' + str(e))
            working.clear()
        finally:
            session.close()
            # end_flag.put('end main process')
            if working.isSet():
                working.clear()
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            # str(time.time() - start_time)
            print('test ended on: ' + current_time)
            shared_data.put('test ended on: ' + current_time)

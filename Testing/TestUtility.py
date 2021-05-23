import threading
import time
from multiprocessing import Queue

from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# # from CbsClasses.CbsPageUtility import CbsPageUtility
# import asyncio

# from concurrent.futures import ThreadPoolExecutor

from CbsClasses.CbsPage import CbsPage
from Testing.CbsPageUtility import CbsPageUtility
from dataBase.DataBase import DataBase, Links

class TestProperties():
    def __init__(self,shared_data: Queue = Queue(), progress_status: Queue = Queue(), end_flag: Queue = Queue(),
             pages=None, session_visible=True):
        self.session_visible = session_visible
        self.shared_data = shared_data
        self.progress_status = progress_status
        self.end_flag = end_flag
        self.pages = pages

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


            driver.implicitly_wait(wait_time)
            return driver
        except WebDriverException as e:
            print('driver error: ' + str(e))
            return None

    @classmethod
    def testPage(cls, page: CbsPage, session: webdriver.Chrome):
        CbsPageUtility.set_statistical_part(page=page, session=session)
        CbsPageUtility.set_sub_subjects(page=page, session=session)
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
        # set up pages for test
        if pages is None:
            try:
                pages_collection = cls.get_pages()
            except Exception as e:
                print('error in loading pages, test is closed')
                shared_data.put('error in loading pages, test is closed')
                working.clear()
                raise e
        else:
            pages_collection = pages
        #set up session for test
        try:
            session = cls.get_sessions()  # default as synchronous test - one instance session
        except Exception as e:
            print('error loading sessions, test is closed')
            shared_data.put('error loading sessions, test is closed')
            working.clear()
            raise e
        # status flow
        shared_data.put('initializing test environment...')
        print('initializing test environment...')
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        shared_data.put('test started on: ' + str(current_time))
        print('test started on: ' + str(current_time))



        error_pages = []
        pages_size = len(pages_collection)
        print('num pages', str(len(pages_collection)))
        shared_data.put('num pages: ' + str(pages_size))

        try:
            for i, page in enumerate(pages_collection):
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

    @classmethod
    def test_with_pyqt_slots(cls,signals=QObject,pages=None):
        # set up pages for test
        if pages is None:
            try:
                pages_collection = cls.get_pages()
                print('pages found in if')
            except Exception as e:
                print('error in loading pages, test is closed')
                signals.status.emit(0)
                signals.finished.emit()
                signals.error.emit(('error in loading pages, test is closed', 'nothing was checked'))
                raise e

        else:
            pages_collection = pages
            print('pages found in else')
        #set up session for test
        try:
            session = cls.get_sessions()  # default as synchronous test - one instance session
            print('sessions found')
        except Exception as e:
            print('error loading sessions, test is closed')
            signals.status.emit(0)
            signals.error.emit(('error loading sessions, test is closed','nothing was checked'))
            signals.finished.emit()
            raise e
        # status flow
        signals.monitor_data.emit('initializing test environment...')
        print('initializing test environment...')
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        signals.monitor_data.emit('test started on: ' + str(current_time))
        print('test started on: ' + str(current_time))



        error_pages = []
        pages_size = len(pages_collection)
        print('num pages', str(len(pages_collection)))
        signals.monitor_data.emit('num pages: ' + str(pages_size))

        try:
            for i, page in enumerate(pages_collection):
                # if not working.isSet():
                #     raise Exception('test canceled')
                    # outside canceled
                signals.monitor_data.emit('ניסיון עברית')
                percents = (i / pages_size)*100
                signals.status.emit(percents)
                print(str("%.1f" % percents) + '%')

                session.get(page.link.url)
                cls.testPage(page, session)

                if len(page.stats_part.errors) > 0:
                    print(page.name, page.link.url)
                    print(page.stats_part.errors)
                    signals.monitor_data.emit(str(page.name))
                    signals.monitor_data.emit(str(page.stats_part.errors))
                    error_pages.append((page.name, page.link.url, page.stats_part.errors))
                else:
                    signals.monitor_data.emit(str(page.name))
                    signals.monitor_data.emit(str(200))

        except Exception as e:
            print('main process stopped due to exception: ' + str(e))
            signals.monitor_data.emit('main process stopped due to exception: ' + str(e))
            # end_flag.put('main process stopped due to exception: ' + str(e))
            signals.finished.emit()
        finally:
            session.close()
            # end_flag.put('end main process')
            # if working.isSet():
            #     working.clear()
            signals.finished.emit()
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            # str(time.time() - start_time)
            print('test ended on: ' + current_time)
            signals.monitor_data.emit('test ended on: ' + current_time)


    @classmethod
    def test_func(cls):

        try:
            pages = cls.get_pages()
        except Exception as e:
            print('error in loading pages, test is closed')

            raise e

        # status flow
        print('initializing test environment...')
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print('test started on: ' + str(current_time))

        try:
            session = cls.get_sessions()  # default as synchronous test - one instance session
        except Exception as e:
            print('error loading sessions, test is closed')
            raise e

        error_pages = []
        pages_size = len(pages)
        print('num pages', str(len(pages)))

        try:
            for i, page in enumerate(pages):
                    # outside canceled
                percents = i / pages_size
                print(str("%.1f" % percents) + '%')

                session.get(page.link.url)
                cls.testPage(page, session)

                if len(page.stats_part.errors) > 0:
                    print(page.name, page.link.url)
                    print(page.stats_part.errors)
                    error_pages.append((page.name, page.link.url, page.stats_part.errors))
                else:
                    pass
        except Exception as e:
            print('main process stopped due to exception: ' + str(e))
        finally:
            session.close()
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            # str(time.time() - start_time)
            print('test ended on: ' + current_time)

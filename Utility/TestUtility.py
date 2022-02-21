import datetime
import os
import sys
import threading
import time
from multiprocessing import Queue

from win32com.client import Dispatch

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchWindowException, \
    StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from CbsObjects.Pages.SubjectPage import SubjectPage
from CbsObjects.TestDetails import TestDetails
from DataBase.DataBase import DataBase, Links
from Utility.Connectivity import Connectivity
from Utility.WebPartUtility import WebPartUtility, ROOT_ELEMENT


class TestUtility:
    @classmethod
    def get_sessions(cls, amount=1, isViseble=True):
        if amount == 1:
            return cls.create_web_driver(isViseble)
        sessions = []
        for i in range(amount):
            sessions.append(cls.create_web_driver(isViseble))
        return sessions

    @classmethod
    def get_he_pages(cls):
        pages = DataBase.get_CBS_he_pages()
        return pages

    @classmethod
    def get_en_pages(cls):
        pages = DataBase.get_CBS_en_pages()
        return pages

    @classmethod
    def _check_chrome_version(cls):
        paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                 r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
        path = list(filter(lambda x: os.path.isfile(x), paths))[0]
        parser = Dispatch("Scripting.FileSystemObject")
        try:
            version = parser.GetFileVersion(path)
            version = version.split('.')[0]
        except Exception:
            print('chrome version is unknown')
            return None
        return version

    @classmethod
    def create_web_driver(cls, withUI=True):
        try:
            ver = cls._check_chrome_version()
            if ver is None:
                raise Exception
            # if ver >

            driver_service = Service(Links.CHROME_DRIVER.value)
            if not withUI:
                options = webdriver.ChromeOptions()
                options.headless(True)
                # # options.add_argument('--disable-gpu')
                driver = webdriver.Chrome(service=driver_service, chrome_options=options)
                # driver = webdriver.Chrome(executable_path=Links.CHROME_DRIVER.value, chrome_options=options)

            else:
                try:
                    driver = webdriver.Chrome(service=driver_service)
                except WebDriverException as e:
                    print('session not created')
                    raise e
                # driver = webdriver.Chrome(executable_path=Links.CHROME_DRIVER.value)

            path = sys.path[1] + '\\DataBase\\LoadTest\\LoadTest.html'
            driver.get(path)

            return driver
        except WebDriverException as e:
            print('driver error: ' + str(e))
            return None

    @classmethod
    def testPage(cls, page: SubjectPage, main_element):

        tests = []
        # WebPartUtility.set_summary(page=page, session=main_element)
        summary = threading.Thread(target=WebPartUtility.set_summary, args=(page, main_element))
        summary.start()
        tests.append(summary)

        # WebPartUtility.set_heb_statistical(page=page, session=main_element)
        statistical = threading.Thread(target=WebPartUtility.set_heb_statistical, args=(page, main_element))
        statistical.start()
        tests.append(statistical)

        # WebPartUtility.set_extra_parts(page=page, root_element=main_element)
        extra_parts = threading.Thread(target=WebPartUtility.set_extra_parts, args=(page, main_element))
        extra_parts.start()
        tests.append(extra_parts)

        # WebPartUtility.set_top_box(page=page, session=main_element)
        top_box = threading.Thread(target=WebPartUtility.set_top_box, args=(page, main_element))
        top_box.start()
        tests.append(top_box)

        # WebPartUtility.set_sub_subjects(page=page, session=main_element)
        sub_subjects = threading.Thread(target=WebPartUtility.set_sub_subjects, args=(page, main_element))
        sub_subjects.start()
        tests.append(sub_subjects)

        # WebPartUtility.set_press_releases(page=page, session=main_element)
        press_releases = threading.Thread(target=WebPartUtility.set_press_releases, args=(page, main_element))
        press_releases.start()
        tests.append(press_releases)

        # WebPartUtility.set_tables_and_charts(page=page, session=main_element)
        tables_and_charts = threading.Thread(target=WebPartUtility.set_tables_and_charts, args=(page, main_element))
        tables_and_charts.start()
        tests.append(tables_and_charts)

        # WebPartUtility.set_tools_and_db(page=page, session=main_element)
        tools_and_db = threading.Thread(target=WebPartUtility.set_tools_and_db, args=(page, main_element))
        tools_and_db.start()
        tests.append(tools_and_db)

        # WebPartUtility.set_publications(page=page, session=main_element)
        publications = threading.Thread(target=WebPartUtility.set_publications, args=(page, main_element))
        publications.start()
        tests.append(publications)

        # WebPartUtility.set_geographic_zone(page=page, session=main_element)
        geographic_zone = threading.Thread(target=WebPartUtility.set_geographic_zone, args=(page, main_element))
        geographic_zone.start()
        tests.append(geographic_zone)

        # WebPartUtility.set_international_comparisons(page=page, session=main_element)
        international_comparisons = threading.Thread(target=WebPartUtility.set_international_comparisons,
                                                     args=(page, main_element))
        international_comparisons.start()
        tests.append(international_comparisons)

        # WebPartUtility.set_more_links(page=page, session=main_element)
        more_links = threading.Thread(target=WebPartUtility.set_more_links, args=(page, main_element))
        more_links.start()
        tests.append(more_links)

        # WebPartUtility.set_conferences_and_seminars(page=page, session=main_element)#TODO
        conferences_and_seminars = threading.Thread(target=WebPartUtility.set_conferences_and_seminars,
                                                    args=(page, main_element))
        conferences_and_seminars.start()
        tests.append(conferences_and_seminars)

        # WebPartUtility.set_videos_links(page=page, session=main_element)#TODO
        videos_links = threading.Thread(target=WebPartUtility.set_videos_links, args=(page, main_element))
        videos_links.start()
        tests.append(videos_links)

        # WebPartUtility.set_pictures_links(page=page, session=main_element)#TODO
        pictures_links = threading.Thread(target=WebPartUtility.set_pictures_links, args=(page, main_element))
        pictures_links.start()
        tests.append(pictures_links)

        for test in tests:
            test.join()
        print("Done threads test in ", page.name)

    # test chronicle order
    @classmethod
    def testPage_(cls, page: SubjectPage, main_element):

        WebPartUtility.set_summary(page=page, session=main_element)

        WebPartUtility.set_heb_statistical(page=page, session=main_element)

        WebPartUtility.set_extra_parts(page=page, root_element=main_element)

        WebPartUtility.set_top_box(page=page, session=main_element)

        WebPartUtility.set_sub_subjects(page=page, session=main_element)

        WebPartUtility.set_press_releases(page=page, session=main_element)

        WebPartUtility.set_tables_and_charts(page=page, session=main_element)

        WebPartUtility.set_tools_and_db(page=page, session=main_element)

        WebPartUtility.set_publications(page=page, session=main_element)

        WebPartUtility.set_geographic_zone(page=page, session=main_element)

        WebPartUtility.set_international_comparisons(page=page, session=main_element)

        WebPartUtility.set_more_links(page=page, session=main_element)

        WebPartUtility.set_conferences_and_seminars(page=page, session=main_element)  # TODO

        WebPartUtility.set_videos_links(page=page, session=main_element)  # TODO

        WebPartUtility.set_pictures_links(page=page, session=main_element)  # TODO

    # visible func
    @classmethod
    def test(cls, shared_data: Queue, progress_status: Queue, end_flag: Queue,
             pages_: list, session_visible: bool = True):

        if pages_ is None:
            try:
                pages = cls.get_he_pages()
            except Exception as e:
                print('error in loading pages, test is closed')
                shared_data.put('error in loading pages, test is closed')
                end_flag.put('error in loading pages, test is closed')
                raise e

        elif type(pages_[0]) == type(1):
            pages = list(filter(lambda x: x.id in pages_, cls.get_he_pages()))
        else:
            print('no action needed')
            print('type page elem: ' + str(type(pages_[0])) + ' type int: ' + str(type(1)))
            pages = pages_
        page_ids = [page.id for page in pages]
        test_details = TestDetails(candidates=page_ids)
        test_details.started()

        # status flow
        shared_data.put(('text', 'initializing test environment...'))
        print('initializing test environment...')
        # t = time.localtime()
        # current_time = time.strftime("%H:%M:%S", t)
        date, time = test_details.start_date()
        shared_data.put(('text', 'test started on: ' + date + ' ' + time))
        print('test started on: ' +  date +' '+ time)

        try:
            session = cls.get_sessions(isViseble=session_visible)  # default as synchronous test - one instance session
        except Exception as e:
            print('error loading sessions, test is closed')
            shared_data.put(('text', 'error loading sessions, test is closed'))
            end_flag.put('error loading sessions, test is closed')
            raise e

        pages_size = len(pages)
        print('num pages', str(len(pages)))
        shared_data.put(('text', 'num pages: ' + str(pages_size)))

        # summary = []
        # summary.append(datetime.date.today().strftime('%d.%m.%y'))  # date
        # summary.append(test_details.start_date())  # test start time
        # summary.append(len(test_details.candidates()))  # number of chosen pages for test
        # summary.append(0)  # counter for checked pages
        # summary.append(0)  # counter for error pages

        try:
            DataBase.init_new_test(test_details)
            for i, page in enumerate(pages):

                if end_flag.qsize() > 0:
                    print('test aborted due to user request:  {}'.format(end_flag.get()))
                    return

                percents = (float(i + 1) / pages_size)
                progress_status.put(percents)
                print(str("%.1f" % percents) + '%')
                try:
                    session.get(page.link.url)

                except WebDriverException as e:
                    print('exception while trying to get page: {}'.format(page.name))
                    if not Connectivity.is_connect():
                        raise e
                    continue
                try:
                    main_element = WebDriverWait(session, 10).until(
                        EC.presence_of_element_located((By.XPATH, ROOT_ELEMENT))
                    )
                    cls.testPage(page, main_element)
                    percents = (float(i + 1) / pages_size) * 100
                except StaleElementReferenceException:
                    try:
                        main_element = WebDriverWait(session, 5).until(
                            expected_conditions.presence_of_element_located(
                                (By.XPATH, "//body[@class='INDDesktop INDChrome INDlangdirRTL INDpositionRight']")))
                        cls.testPage(page, main_element)

                    except Exception:
                        page.stats_part.errors.append('unknown error')
                        break
                except TimeoutException:
                    print("Timed out waiting for page to load: {}".format(page.name))
                    DataBase.save_test_result(test_details.key(), page)
                    continue
                except NoSuchWindowException:
                    page.stats_part.errors.append("couldn't find root element")
                    DataBase.save_test_result(test_details.key(), page)
                    continue
                # summary[3] += 1
                if len(page.get_errors()) > 0:
                    # print(page.name, page.link.url)
                    print(page.error_to_str())
                    shared_data.put(('link', page.name, page.link.url, 'Fail'))
                    shared_data.put(('text', page.error_to_str()))
                    # outer_signals.page_info.emit(str({'name': page.name, 'url': page.link.url, 'error': True}))
                    # outer_signals.monitor_data.emit(str(page.error_to_str().replace('\n', '<br>')))
                    # error_pages.append((page.name, page.link.url, page.error_to_str()))
                    DataBase.save_test_result(test_details.key(), page)
                    # summary[4] += 1
                else:
                    shared_data.put(('link', page.name, page.link.url, 'Pass'))

                test_details.add_scanned_page(page.id)
        except NoSuchWindowException as e:
            print('Main test stopped due to unexpected  session close')
            shared_data.put(('text', 'Main test stopped due to unexpected  session close'))           # outer_signals.monitor_data.emit('Main test stopped due to unexpected  session close')
            end_flag.put('unexpected  session close')
            raise e

        except Exception as e:
            print('main process stopped due to exception: ' + str(e))
            shared_data.put(('text', 'main process stopped due to exception: ' + str(e)))
            end_flag.put('unexpected  session close')
            raise e

        finally:
            session.close()
            test_details.ended()
            end_flag.put('session close')
            end_date,end_time = test_details.end_date()
            print('test ended on: ' + end_time)
            shared_data.put(('test', 'test ended on: ' + end_time))
            DataBase.save_test_result(test_details.key(), page)
            # DataBase.save_summary_result(test_details.key(), summary)

    @classmethod
    def get_test_result(cls, log_key):
        file_key = log_key
        return DataBase.get_test_result(file_key=file_key)

    @classmethod
    def get_test_result_as_pdf(cls, log_key):
        file_key = log_key
        return DataBase.get_pdf_test_result(file_key=file_key)


# for browser version match with the automation driver
paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
         r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
path = list(filter(lambda x: os.path.isfile(x), paths))[0]
parser = Dispatch("Scripting.FileSystemObject")
try:
    version = parser.GetFileVersion(path)
    version = version.split('.')[0]
    print(version)
except Exception:
    print('chrome version is unknown')

# class TestProperties():
#     def __init__(self, shared_data: Queue = Queue(), progress_status: Queue = Queue(), end_flag: Queue = Queue(),
#                  pages=None, session_visible=True):
#         self.session_visible = session_visible
#         self.shared_data = shared_data
#         self.progress_status = progress_status
#         self.end_flag = end_flag
#         self.pages = pages

# for certificate recognition in requests
##########
import threading

import certifi
# import ssl
##########
from urllib.error import URLError
from itertools import cycle
import urllib3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import MaxRetryError

from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from CbsObjects.WebPartLine import WebPartLine
from DataBase.DataBase import Links

import urllib.request

class ConnectionPool:
    def __init__(self):
        self.pool = [urllib3.PoolManager(ca_certs=certifi.where(),maxsize=100, block=True) for i in range(20)]
        self.iterator = cycle(self.pool) # cycle iterator for reuse connections

    def request(self,method,url,redirect):
        return next(self.iterator).request(method=method,url=url,redirect=redirect)

HTTPS = ConnectionPool()
# HTTPS = urllib3.PoolManager(ca_certs=certifi.where(),maxsize=100, block=True)

# CERT_CONTEXT = ssl.create_default_context(cafile=certifi.where())
CBS_HOME_PAGE_NAME = 'דף הבית'
CBS_404_TEXTS = ['מתנצלים, הדף לא נמצא', 'Sorry, the page is not found']
CBS_403_TEXTS = ['שלום, אנו מצטערים, הגישה לדף זה נחסמה בשל פעולה לא מורשית', 'Block ID: 5578236093159424155',
                 'מספר חסימה']
XPATH = {
    "HEBREW_STATS_XPATH": Links.HEBREW_STATS_XPATH.value,
    "RIGHT_EXTRA_PARTS_XPATH": Links.RIGHT_EXTRA_PARTS_XPATH.value,
    "LEFT_EXTRA_PARTS_XPATH": Links.LEFT_EXTRA_PARTS_XPATH.value,
    "TOOLS_AND_DB_XPATH": Links.TOOLS_AND_DB_XPATH.value,
    "SUMMARY_XPATH": Links.SUMMARY_XPATH.value,
    "TOP_BOX_XPATH": Links.TOP_BOX_XPATH.value,
    "SUB_SUBJECTS_XPATH": Links.SUB_SUBJECTS_XPATH.value,
    "PRESS_RELEASES_XPATH": Links.PRESS_RELEASES_XPATH.value,
    "TABLES_AND_CHARTS_XPATH": Links.TABLES_AND_CHARTS_XPATH.value,
    "PUBLICATIONS_XPATH": Links.PUBLICATIONS_XPATH.value,
    "INTERNATIONAL_COMPARISONS_XPATH": Links.INTERNATIONAL_COMPARISONS_XPATH.value,
    "MORE_LINKS_XPATH": Links.MORE_LINKS_XPATH.value,
    "GEOGRAPHIC_ZONE_XPATH": Links.GEOGRAPHIC_ZONE_XPATH.value}
ROOT_ELEMENT = Links.ROOT_XPATH.value


class WebPartUtility:
    # returns the element from web page which contains the web-part component
    @classmethod
    def get_main_element(cls, type, session: webdriver.Chrome):
        try:
            xpath ='.'+XPATH[type]
        except Exception as e:
            print('exception while trying to get xpath from dict: ', e)
            return None, 'exception while trying to get xpath from dict: {}'.format(e)
        try:
            main_element = WebDriverWait(session, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            # main_element = session.find_element(By.XPATH, xpath)
            if not main_element.is_displayed():
                return None, 'Hidden'
        except TimeoutException as e:

            return None, 'TimeoutException in get main_element'
        except NoSuchElementException as e:

            return None, 'NoSuchElementException'
        except WebDriverException:
            print('chrome session error, consider restart your program and check your driver configuration')
            return None, 'chrome session error'
        except Exception as e:
            print('unknown exception while trying to get xpath for: ', str(type), ' exception: ', e)

            return None, 'Exception'
        return main_element, None

    # only for hebrew page
    @classmethod
    def set_heb_statistical(cls, page: SubjectPage, session: WebDriver):
        print('statistical test in: {}'.format(page.name))
        log_test = 0
        # check if the element located
        root_element, error = cls.get_main_element('HEBREW_STATS_XPATH', session)
        if root_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
            print('stats  not tested in: ', page.name, ', {}'.format(error))
            return
        # check id not displayed
        try:
            is_hidden = root_element.find_element(By.XPATH,
                                                  "./div[@class='ms-webpart-chrome ms-webpart-chrome-fullWidth ']")
            print('stats not displayed and not tested in: ', page.name)
            return
        except NoSuchElementException:
            log_test += 1
            pass

        # title check
        try:
            title = root_element.find_element(By.XPATH, "./h2/nobr/span")
            title = title.text
            if not title == 'עלוני סטטיסטיקל':
                print('title in stats is: ', title)
                page.stats_part.errors.append('title not correct')
            log_test += 1
        except NoSuchElementException:
            page.stats_part.errors.append('title not correct')
            print('stats not contain any title: ', page.name)
            return

        images = root_element.find_elements(By.XPATH, "./ul/li/div/div/img")
        links = root_element.find_elements(By.XPATH, "./ul/li/div/div[3]/a")
        # print('num images: {}, num links: {}'.format(len(images),len(links)))
        if len(images) == 0:
            page.stats_part.errors.append('images content is missing')
        else:
            images, errors = PageUtility.set_url_links(images, attrib='src')
            errors = [error + ' in Statistical image' for error in errors]
            page.stats_part.errors.extend(errors)
            log_test += 1
            # page.stats_part.images.extend(links)

        if len(links) == 0:
            page.stats_part.errors.append('links content is missing')
        else:
            links, errors = PageUtility.set_url_links(links)
            errors = [error + ' ' for error in errors]
            page.stats_part.errors.extend(errors)
            log_test += 1
            # page.stats_part.links.extend(links)

            # *****************************************************************************************************************
        try:
            all_stats_link = root_element.find_element(By.XPATH, "./a")
        except NoSuchElementException:
            page.stats_part.errors.append('link to all massages is missing')
            return
        # text test
        text = all_stats_link.text
        if not text == 'לכל עלוני הסטטיסטיקל >':
            page.stats_part.errors.append('text in link to all massages not correct')

        cur_link = CbsLink(all_stats_link.get_attribute('href'))
        PageUtility.set_link_status(cur_link)
        if not cur_link.status_code == 200:
            page.stats_part.errors.append('link to all massages is broken')
        print('stats ended in: {} with {} checks'.format(page.name, log_test))

    @classmethod
    def set_top_box(cls, page: SubjectPage, session: webdriver.Chrome):
        print('top-box test in: {}'.format(page.name))
        main_element, error = cls.get_main_element('TOP_BOX_XPATH', session)
        if main_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
            print('top_box not tested in: ', page.name, ', {}'.format(error))
            return

        elements = main_element.find_elements(By.XPATH, "./div[@class='categoryBox']")
        elements = list(
            map(lambda e: e.find_element(By.XPATH, "./a"),
                filter(lambda x: x.is_displayed(), elements)))
        # elements = [element.find_element_by_xpath(".//a") for element in elements]

        if len(elements) == 0:  # inside elements are not displayed
            page.top_box.errors.append('top box is displayed without any data')
            return

        else:
            links, errors = PageUtility.set_url_links(elements)
            # page.top_box.links.extend(links)
            errors = [error + ' ' for error in errors]
            # errors = list(map(lambda x:x+' in top box',errors))
            page.top_box.errors.extend(errors)

    @classmethod
    def set_more_links(cls, page: SubjectPage, session: webdriver.Chrome):
        print('more-links test in: {}'.format(page.name))

        # check if the element located
        root_element, error = cls.get_main_element('MORE_LINKS_XPATH', session)
        if root_element is None:
            print('more links not tested')
            if error == 'chrome session error':
                raise Exception('chrome session error')
            print('more links not tested in: ', page.name, ', {}'.format(error))
            return

        # title check
        title = root_element.find_element(By.XPATH, "./h2/span").text
        if not title == 'קישורים נוספים':
            page.more_links.errors.append('title is not correct')

        # inside links check
        links = root_element.find_elements(By.XPATH, "./ul/div/div/div/div/ul/li/div/div[1]/a")
        # links = list(map(lambda li: CbsLink(url=li.get_attribute('href'), page_name=li.text), links))
        if len(links) < 1:
            page.more_links.errors.append('no content ')
        links, errors = PageUtility.set_url_links(links)
        # page.press_releases.links.extend(links)
        page.more_links.errors.extend(errors)

    @classmethod
    def set_sub_subjects(cls, page: SubjectPage, session: webdriver.Chrome):
        print('sub-subjects test in: {}'.format(page.name))

        # check if the element located
        root_element, error = cls.get_main_element('SUB_SUBJECTS_XPATH', session)
        if root_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
            print('sub-subjects not tested in: ', page.name, ', {}'.format(error))
            return

        # check title
        try:
            title = root_element.find_element(By.XPATH, "./h2[@class='ms-webpart-titleText']/span").text

            if not title == 'נושאי משנה':
                print('title is: ', title)
                page.sub_subjects.errors.append('title is not correct')
        except NoSuchElementException as e:
            print('Exception: ', e, " in sub-subject, page: ", page.name)
            page.sub_subjects.errors.append('title is not correct')
        except TimeoutException as e:
            print('Exception: ', e, " in sub-subject, page: ", page.name)
            page.sub_subjects.errors.append('title is not correct')

        # find all the links inside and set their status
        links = root_element.find_elements(By.XPATH, "./ul[@class='subtopicsList']/li/a")
        if len(links) == 0:
            page.sub_subjects.errors.append('no internal links')
            return
        links, errors = PageUtility.set_url_links(links)
        errors = [error + ' ' for error in errors]
        page.sub_subjects.errors.extend(errors)
        # page.stats_part.links.extend(links)

    @classmethod
    def set_press_releases(cls, page: SubjectPage, session: webdriver.Chrome):
        print('press-releases test in: {}'.format(page.name))

        # when this web part is not displayed the style is "display: none;" and -> text "הודעות לתקשורת"
        # is not exist thus the element wouldn't be found and the function will return

        root_element, error = cls.get_main_element(type='PRESS_RELEASES_XPATH', session=session)
        if root_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
            print('press_releases not tested in: ', page.name, ', {}'.format(error))
            return

        # title check
        try:
            title = root_element.find_element(By.XPATH, './h2/span')
            title = title.text
            if not title == 'הודעות לתקשורת':
                page.press_releases.errors.append('title is not correct')
        except NoSuchElementException:
            print('press_releases title fail in: ', page.name)
            page.press_releases.errors.append('title is not correct')

        # inside links check
        try:
            links = root_element.find_elements(By.XPATH, "./div[@id='Control_List_Subject_Link']/ul/li/div/div/a")
            if len(links) == 0:
                page.press_releases.errors.append('no content inside')
                return
            links, errors = PageUtility.set_url_links(links)
            page.press_releases.links.extend(links)
            page.press_releases.errors.extend(errors)
        except TimeoutException:
            page.press_releases.errors.append('no found any content')
            return
        except NoSuchElementException:
            page.press_releases.errors.append('no found any content')
            return

        # last link test
        try:
            to_all_massages = root_element.find_element(By.XPATH, "./div/a")
            # text = to_all_massages.text
            # if not text == ' לכל ההודעות לתקשורת <':
            #     print('press r last link text: ', text)
            #     page.press_releases.errors.append('text not correct in last link')
            cur_link = CbsLink(to_all_massages.get_attribute('href'))
            PageUtility.set_link_status(cur_link)
            if not cur_link.status_code == 200:
                page.press_releases.errors.append('link to all massages is broken')
        except TimeoutException:
            return
        except NoSuchElementException:
            page.press_releases.errors.append('link to all massages not found')
            return

    @classmethod
    def set_publications(cls, page: SubjectPage, session: webdriver.Chrome):
        print('publications test in: {}'.format(page.name))

        # check if the element located
        root_element, error = cls.get_main_element('PUBLICATIONS_XPATH', session)
        if root_element is None:

            if error == 'chrome session error':
                raise Exception('chrome session error')
            print('publications not tested in: ', page.name, ', {}'.format(error))

            return

        # check title
        try:
            title = root_element.find_element(By.XPATH, './h2/span').text
            if not title == 'פרסומים':
                page.publications.errors.append('title is not correct')

        except NoSuchElementException:
            page.publications.errors.append('title is not correct')
        except TimeoutException:
            page.publications.errors.append('title is not correct')

        # check links inside
        try:
            links = root_element.find_elements(By.XPATH, './div/ul/li/div/div/a')
            if len(links) < 1:
                page.publications.errors.append('no content')
            else:
                links, errors = PageUtility.set_url_links(links)
                errors = [error + ' ' for error in errors]
                page.publications.errors.extend(errors)

        except NoSuchElementException:
            page.publications.errors.append('title is not correct')
        except TimeoutException:
            page.publications.errors.append('title is not correct')

        # check last link
        try:
            link = root_element.find_element(By.XPATH, "./div/a")
            link = CbsLink(link.get_attribute('href'))
            PageUtility.set_link_status(link)
            # link, errors = PageUtility.set_url_links([link])
            # if len(errors) > 0:
            #     page.publications.errors.append("last link problem")
            #     return
            if not link.status_code == 200:
                page.publications.errors.append("last link is broken")

        except Exception as e:
            print("publication last link exception {}".format(e))
            page.publications.errors.append("last link problem")

    @classmethod
    def set_extra_parts(cls, page: SubjectPage, root_element):
        print('extra-parts test in: {}'.format(page.name))

        # check if left element located
        left_element, error = cls.get_main_element('LEFT_EXTRA_PARTS_XPATH', root_element)
        if left_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
            return
        else:
            page.extra_error_parts.errors.append('left side of the page contains wrong web parts')

        # check if right element located
        right_element, error = cls.get_main_element('RIGHT_EXTRA_PARTS_XPATH', root_element)
        if right_element is None:
            print('right errors not found')
            if error == 'chrome session error':
                raise Exception('chrome session error')
            return
        else:
            page.extra_error_parts.errors.append('right side of the page contains wrong web parts')

    @classmethod
    def set_tools_and_db(cls, page: SubjectPage, session):
        print('tools-and-db test in: {}'.format(page.name))

        # check if the element located
        root_element, error = cls.get_main_element('TOOLS_AND_DB_XPATH', session)
        if root_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
            print('tools_and_db not tested in: ', page.name, ', {}'.format(error))

            return

        # title test
        try:
            title = root_element.find_element(By.XPATH, "./div/h2/span")
            title = title.text
            if not title == 'כלים ומאגרי נתונים':
                # print('title in tadb is: ', title)
                page.tools_and_db.errors.append('title not correct')
        except NoSuchElementException:
            page.tools_and_db.errors.append('title not correct')
            print('tools_db not contain any title: ', page.name)

        # image test
        try:
            image = root_element.find_element(By.XPATH, "./div/div/div/img")
            image = CbsLink(url=image.get_attribute('src'))
            PageUtility.set_link_status(image)
            if not image.status_code == 200:
                page.tools_and_db.errors.append('image is broken')

        except NoSuchElementException:
            page.tools_and_db.errors.append('no image')
        except TimeoutException:
            page.tools_and_db.errors.append('no image')
        except Exception as e:
            print('exception in tools and DB')
            raise e

        # link test
        try:
            link = root_element.find_element(By.XPATH, "./div/div/div/a")
            link = CbsLink(link.get_attribute('href'))
            PageUtility.set_link_status(link)
            if not link.status_code == 200:
                page.tools_and_db.errors.append('link is broken')

        except NoSuchElementException:
            page.tools_and_db.errors.append('no link')
        except TimeoutException:
            page.tools_and_db.errors.append('no link')
        except Exception as e:
            print('exception in tools and DB')
            raise e
        return

    @classmethod
    def set_summary(cls, page: SubjectPage, session: webdriver):
        print('summary test in: {}'.format(page.name))
        # summary = session.find_element_by_xpath(Links.SUMMARY_XPATH.value)
        # check if the element located
        root_element, error = cls.get_main_element('SUMMARY_XPATH', session)
        if root_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
            return
        # paragraphs test
        paragraphs = root_element.find_elements(By.XPATH, "./div[4]/p")



    @classmethod
    def set_tables_and_charts(cls, page: SubjectPage, session: webdriver):
        print('tables-and-charts test in: {}'.format(page.name))

        # check if the element located
        root_element, error = cls.get_main_element('TABLES_AND_CHARTS_XPATH', session)
        if root_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
            return

        # title check
        try:

            title = root_element.find_element(By.XPATH, "./h2/span").text
            if not title == 'לוחות ותרשימים':
                page.tables_and_charts.errors.append('title is not correct')
                print(title)

        except NoSuchElementException as e:
            print('no title in tables and charts')
            page.tables_and_charts.errors.append('no title')
            return
        except TimeoutException as e:
            print('no title in tables and charts')
            page.tables_and_charts.errors.append('no title')
            return
        except Exception:
            print('not recognized exception in tables and charts')
            return

        # links check
        links = root_element.find_elements(By.XPATH, "./div/ul/li/div/div[1]/a")
        # images check
        images = root_element.find_elements(By.XPATH, "./div/ul/li/div/div[1]/a/img")

        if not links:
            page.tables_and_charts.errors.append('links are missing')
        else:
            links, errors = PageUtility.set_url_links(links)
            page.tables_and_charts.errors.extend(errors)

            if not images:
                page.tables_and_charts.errors.append('icons are missing')
            else:
                images, errors = PageUtility.set_url_links(images,attrib='src')
                errors = [error + ' ' for error in errors]
                page.tables_and_charts.errors.extend(errors)

        # last link check
        try:
            to_all_maps = root_element.find_element(By.XPATH, "./div[1]/a[@class='MadadTableMapsToAll']")
            to_all_maps = CbsLink(to_all_maps.get_attribute('href'))
            PageUtility.set_link_status(to_all_maps)
            if not to_all_maps.status_code == 200:
                page.tables_and_charts.errors.append('last link is broken')

        except Exception as e:
            page.tables_and_charts.errors.append('to all charts link is missing')
            print('exception in set_tables_and_charts: {}'.format(e))

    @classmethod
    def set_geographic_zone(cls, page: SubjectPage, session: webdriver):
        print('geographic-zone test in: {}'.format(page.name))

        # check if the element located
        root_element, error = cls.get_main_element('GEOGRAPHIC_ZONE_XPATH', session)
        if root_element is None:
            print('geographic zone not exist in {}'.format(page.name))
            if error == 'chrome session error':
                raise Exception('chrome session error')
            return

        # check link status
        try:
            a = root_element.find_element(By.XPATH, './div/a').get_attribute('href')
            link = CbsLink(url=a)
            PageUtility.set_link_status(link)
            if not link.status_code == 200:
                page.geographic_zone.errors.append('link is broken')
            # else:
            #     print('link is ok')
            # print('status: ', link.status_code)
        except NoSuchElementException as e:
            page.geographic_zone.errors.append('no link in geographic zone')
            print('no geographic_zone', e)
            return
        except TimeoutException as e:
            page.geographic_zone.errors.append('no link in geographic zone')
            print('no geographic_zone', e)
            return

        except Exception as e:
            page.geographic_zone.errors.append('no link in geographic zone')
            print('not recognized exception in geographic_zone', e)
            return

    @classmethod
    def set_international_comparisons(cls, page: SubjectPage, session: webdriver.Chrome):
        print('international-comparisons test in: {}'.format(page.name))

        # check if the element located
        root_element, error = cls.get_main_element('INTERNATIONAL_COMPARISONS_XPATH', session)
        if root_element is None:
            print('geographic zone not exist in {}'.format(page.name))
            if error == 'chrome session error':
                raise Exception('chrome session error')
            return

        # check link status
        try:
            # a = main_element.find_element(by=By.XPATH, value="./div/a").get_attribute('href')
            a = root_element.find_element(By.XPATH, './div/a').get_attribute('href')
            link = CbsLink(url=a)
            PageUtility.set_link_status(link)
            if not link.status_code == 200:
                page.international_comparisons.errors.append('link is broken')
            # else:
            #     print('link is ok')
            # print('status: ', link.status_code)
        except NoSuchElementException as e:
            page.international_comparisons.errors.append('no link')
            print('no international_comparisons', e)
            return
        except TimeoutException as e:
            page.international_comparisons.errors.append('no link')
            print('no international_comparisons', e)
            return

        except Exception as e:
            page.international_comparisons.errors.append('no link')
            print('not recognized exception in international_comparisons', e)
            return

    @classmethod
    def set_conferences_and_seminars(cls, page, session):
        print('conferences-and-seminars test in: {}'.format(page.name))
        print('in developing process')

    @classmethod
    def set_videos_links(cls, page, session):
        print('video-links test in: {}'.format(page.name))
        # check if the element located
        root_element, error = cls.get_main_element('HEBREW_STATS_XPATH', session)
        if root_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
            print('stats  not tested in: ', page.name, ', {}'.format(error))
            return
        print('in developing process')

    @classmethod
    def set_pictures_links(cls, page, session):
        print('pictures-links test in: {}'.format(page.name))
        print('in developing process')

    @classmethod
    def set_slideshows(cls, page, session):
        #todo
        pass


class PageUtility:

    @classmethod
    def create_pages(cls, link_list):
        return [SubjectPage(link, link.name) for link in link_list]

    @classmethod
    def create_minimal_pages(cls, link_list):
        pages = []
        for link in link_list:
            pages.append(SubjectPage(link[0], link[1]))
        return pages

    @classmethod
    def set_link_status(cls, link: CbsLink):
        resp = None
        try:
            resp = HTTPS.request('GET', link.url, True)
            link.status_code = resp.status

        except TimeoutException:
            link.status_code = 408
            return
        except URLError as e:
            print('URLError in set_link_status: ', e)
            print('link: ', link.url)
            link.status_code = 404
            return
        except MaxRetryError as e:
            if link.url == 'https://stats.oecd.org/':
                link.status_code = 200
            else:
                link.status_code = 404
            return
        except Exception as e:
            print('set link status func unknown exception', e)
            link.status_code = 408
            return
        finally:
            # case everything went well - still need to check default error page of CBS
            # and link.url.endswith('.aspx')
            if resp and link.status_code == 200 and link.type == 'page':
                # print('inside deep check: ')
                # print(link.url)
                content = resp.data.decode('utf-8')
                resp.release_conn()
                # print('content: ', content)
                cls.check_for_cbs_error_page(content, link)
                return



    @classmethod
    def link_state(cls, element, attrib, link_list, errors, iteration):
        url = element.get_attribute(attrib)
        link = CbsLink(url)
        cls.set_link_status(link)
        link_list.append(link)
        if not link.status_code == 200:
            print(str(link.status_code) + str(link.url))
            errors.append(str(iteration + 1) + 'th link is broken')

    # gets <a> or <img> web elements and check them for errors
    # returns tuple of list of CBS links from input and list of errors -
    # each error describes the index of the error link
    @classmethod
    def set_url_links(cls, links: [WebElement], attrib='href'):
        link_list = []
        errors = []
        threads = []
        for i, element in enumerate(links):
            t = threading.Thread(target=cls.link_state, args=(element,attrib,link_list,errors,i))
            threads.append(t)
            t.start()

            # url = element.get_attribute(attrib)
            # link = CbsLink(url)
            # cls.set_link_status(link)
            # link_list.append(link)
            # if not link.status_code == 200:
            #     print(str(link.status_code) + str(link.url))
            #     errors.append(str(i + 1) + 'th link is broken')
        for t in threads:
            t.join()

        return link_list, errors

    @classmethod
    def check_for_cbs_error_page(cls, content, link: CbsLink):
        # print('start deep check')
        for error_text in CBS_404_TEXTS:
            if error_text in str(content):
                link.status_code = 404
                return True
        for error_text in CBS_403_TEXTS:
            if error_text in str(content):
                link.status_code = 403
                return True
        # print('end deep check')
        return False

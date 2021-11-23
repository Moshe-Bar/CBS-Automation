# for certificate recognition in requests
##########
import certifi
# import ssl
##########
from urllib.error import URLError

import urllib3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.remote.webelement import WebElement

from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from CbsObjects.WebPartLine import WebPartLine
from DL.DataBase import Links

from temp.Language import Language
import urllib.request

HTTPS = urllib3.PoolManager(ca_certs=certifi.where())
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
    "MORE_LINKS_XPATH" : Links.MORE_LINKS_XPATH.value}


class WebPartUtility:
    # returns the element from web page which contains the web-part component
    @classmethod
    def get_main_element(cls, type, session: webdriver.Chrome):
        try:
            xpath = XPATH[type]
        except Exception as e:
            print('exception while trying to get xpath from dict: ', e)
            return None, 'exception while trying to get xpath from dict: {}'.format(e)
        try:
            main_element = session.find_element(By.XPATH, xpath)
            if not main_element.is_displayed():
                return None, 'Hidden'
        except TimeoutException:
            return None, 'TimeoutException'
        except NoSuchElementException:
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

        # check if the element located
        root_element, error = cls.get_main_element('HEBREW_STATS_XPATH', session)
        if root_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
            return

        # check id not displayed
        try:
            is_hidden = root_element.find_element(By.XPATH, "./div[@class='ms-webpart-chrome ms-webpart-chrome-fullWidth ']")
            print('stats not displayed and not tested in: ', page.name)
            return
        except NoSuchElementException:
            pass


        # title check
        try:
            title = root_element.find_element(By.XPATH, "./h2/nobr/span")
            title = title.text
            if not title == 'עלוני סטטיסטיקל':
                print('title in stats is: ',title)
                page.stats_part.errors.append('title not correct')
        except NoSuchElementException:
            page.stats_part.errors.append('title not correct')
            print('stats not contain any title: ',page.name)
            return



        images = root_element.find_elements(By.XPATH, ".//ul[@class='cbs-List']//li//img")
        links = root_element.find_elements(By.XPATH, ".//ul[@class='cbs-List']//li//a")

        if len(images) == 0 or len(links) == 0:
            page.stats_part.errors.append('images or links content is missing')
        else:
            images, errors = PageUtility.set_url_links(images, attrib='src')
            errors = [error + ' in Statistical image' for error in errors]
            page.stats_part.errors.extend(errors)
            # page.stats_part.images.extend(links)

        if len(links) == 0:
            page.stats_part.errors.append('links content is missing')
        else:
            links, errors = PageUtility.set_url_links(links)
            errors = [error + ' ' for error in errors]
            page.stats_part.errors.extend(errors)
            page.stats_part.links.extend(links)

            # *****************************************************************************************************************
        try:
            all_stats_link = root_element.find_element(By.XPATH,"./a")
        except NoSuchElementException:
            page.stats_part.errors.append('link to all massages is missing')
            return
        # text test
        text = all_stats_link.text
        if not text =='לכל עלוני הסטטיסטיקל >':
            page.stats_part.errors.append('text in link to all massages not correct')

        cur_link = CbsLink(all_stats_link.get_attribute('href'))
        # page.stats_part.links.append(cur_link)
        PageUtility.set_link_status(cur_link)
        if not cur_link.status_code == 200:
            page.stats_part.errors.append('link to all massages is broken')

    @classmethod
    def set_top_box(cls, page: SubjectPage, session: webdriver.Chrome):
        print('top-box test in: {}'.format(page.name))
        main_element, error = cls.get_main_element('TOP_BOX_XPATH', session)
        if main_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
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
            return

        # title check
        title = root_element.find_element(By.XPATH, "./h2//span").text
        if not title == 'קישורים נוספים':
            page.more_links.errors.append('title is not correct')

        # inside links check
        links = root_element.find_elements(By.XPATH, "./ul/div/div/div/div/ul/li/div/div[@class='link-item']/a")
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
            print('sub-subjects not tested')
            if error == 'chrome session error':
                raise Exception('chrome session error')
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

    #todo
    @classmethod
    def set_press_releases(cls, page: SubjectPage, session: webdriver.Chrome):
        print('press-releases test in: {}'.format(page.name))

        # when this web part is not displayed the style is "display: none;" and -> text "הודעות לתקשורת"
        # is not exist thus the element wouldn't be found and the function will return

        root_element, error = cls.get_main_element(type='PRESS_RELEASES_XPATH', session=session)
        if root_element is None:
            if error == 'chrome session error':
                raise Exception('chrome session error')
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
            text =  to_all_massages.text
            if not text == ' לכל ההודעות לתקשורת >':
                print('press r last link text: ',text)
                page.press_releases.errors.append('text not correct in last link')
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
            print('publication not tested')
            if error == 'chrome session error':
                raise Exception('chrome session error')
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
            links = root_element.find_elements(By.XPATH, './div//ul/li/div/div/a')
            if len(links) <1:
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
            link = root_element.find_element(By.XPATH,"./a")
            link, errors = PageUtility.set_url_links([link])
            if len(errors)>0:
                page.publications.errors.append("last link problem")
                return

        except Exception as e:
            page.publications.errors.append("last link problem")


    @classmethod
    def set_extra_parts(cls, page: SubjectPage, root_element):
        print('extra-parts test in: {}'.format(page.name))

        # left side of the page
        try:
            left_extra_parts = root_element.find_element(By.XPATH, Links.LEFT_EXTRA_PARTS_XPATH.value)
            page.extra_error_parts.errors.append('left side of the page contains wrong web parts')
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        # right side of the page
        try:
            right_extra_parts = root_element.find_element(By.XPATH, Links.RIGHT_EXTRA_PARTS_XPATH.value)
            page.extra_error_parts.errors.append('right side of the page contains wrong web parts')
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        return

    @classmethod
    def set_tools_and_db(cls, page: SubjectPage, session):
        print('tools-and-db test in: {}'.format(page.name))

        # left side of the page
        try:
            tools_and_db = session.find_element(By.XPATH, Links.TOOLS_AND_DB_XPATH.value)
            title = session.find_element(By.XPATH, "//h2[@id='WpTitleToolAndDataBasesLinks']//span").text
            images = session.find_elements(By.XPATH, Links.TOOLS_AND_DB_XPATH.value + "//img")
            links = session.find_elements(By.XPATH, Links.TOOLS_AND_DB_XPATH.value + "//a")

            # test image
            if len(images) == 0:
                page.stats_part.errors.append('image content is missing')
            else:
                for i, img in enumerate(images):
                    cur_link = CbsLink(img.get_attribute('src'))
                    PageUtility.set_link_status(cur_link)
                    page.tools_and_db.images.append(cur_link)
                    if not cur_link.status_code == 200:
                        page.tools_and_db.errors.append('image is broken')
                        page.isCorrect = False

            # test links
            if len(links) == 0:
                page.stats_part.errors.append('link content is missing')
                page.isCorrect = False
            else:
                for i, sheet in enumerate(links):
                    cur_link = CbsLink(sheet.get_attribute('href'))
                    page.tools_and_db.links.append(cur_link)
                    PageUtility.set_link_status(cur_link)
                    if not cur_link.status_code == 200:
                        page.tools_and_db.errors.append('link is broken')
                        page.isCorrect = False

            # test title
            if not title == 'כלים ומאגרי נתונים':
                print(title)
                page.tools_and_db.errors.append('title i not correct')
                print('title is not correct')

        except TimeoutException:
            pass
        except NoSuchElementException:
            pass
        except Exception as e:
            print('exception in tools and DB')
            raise e
        return

    @classmethod
    def set_summary(cls, page: SubjectPage, session: webdriver):
        print('summary test in: {}'.format(page.name))
        try:
            # summary = session.find_element_by_xpath(Links.SUMMARY_XPATH.value)
            paragraph = session.find_element(By.XPATH, Links.SUMMARY_XPATH.value).text
            images = session.find_elements(By.XPATH, Links.SUMMARY_XPATH.value + "//img")
            links = session.find_elements(By.XPATH, Links.SUMMARY_XPATH.value + "//a")
            # check text is exist
            if paragraph == '':
                page.summary.errors.append('no text')

            # test images
            if len(images) > 0:
                counter = 0
                for i, img in enumerate(images):
                    cur_link = CbsLink(img.get_attribute('src'))
                    PageUtility.set_link_status(cur_link)
                    page.summary.images.append(cur_link)
                    if not cur_link.status_code == 200:
                        counter += 1

                if counter > 1:
                    page.summary.errors.append('{} images are broken'.format(counter))
                elif counter == 1:
                    page.summary.errors.append('{} image is broken'.format(counter))

            # test links
            if len(links) > 0:
                counter = 0
                for i, url in enumerate(links):
                    cur_link = CbsLink(url.get_attribute('href'))
                    PageUtility.set_link_status(cur_link)
                    page.summary.links.append(cur_link)
                    if not cur_link.status_code == 200:
                        counter += 1

                if counter > 1:
                    page.summary.errors.append('{} links is broken'.format(counter))
                elif counter == 1:
                    page.summary.errors.append('{} link is broken'.format(counter))

        except TimeoutException:
            pass
        except NoSuchElementException:
            print("summary couldn't be found")
        except Exception as e:
            print('exception in summary test')
        return

    @classmethod
    def set_tables_and_charts(cls, page: SubjectPage, session: webdriver):
        print('tables-and-charts test in: {}'.format(page.name))

        try:
            element: WebElement = session.find_element(By.XPATH, Links.TABLES_AND_CHARTS_XPATH.value)
        except NoSuchElementException as e:
            print('no tables and charts', e)
            return
        except TimeoutException as e:
            print('no tables and charts', e)
            return
        except TypeError as e:
            print('exception, xpath is not recognized', e)
            return
        except Exception as e:
            print('not recognized exception in tables and charts', e)
            return

        # title check
        try:

            title = element.find_element(By.XPATH, ".//h2//span").text
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
        except TypeError as e:
            print('exception, xpath is not recognized')
            return
        except Exception:
            print('not recognized exception in tables and charts')
            return

        # links check
        try:

            li_elements = element.find_elements(By.XPATH, ".//div//ul//li")
            print('number li: ', len(li_elements))
            web_part_lines = []
            if len(li_elements) == 0:
                raise NoSuchElementException(msg='elements not found')

            for li in li_elements:
                div = li.find_elements(By.XPATH, ".//div//div")
                pic_url = CbsLink(div[0].find_element(By.XPATH, ".//a//img").get_attribute('src'))
                link_url = CbsLink(div[0].find_element(By.XPATH, ".//a").get_attribute('href'))
                name = div[0].text
                date = div[1].text
                web_part_lines.append(WebPartLine(link_url, pic_url, date, name))

            cls.check_lines(web_part_lines, page.tables_and_charts.errors)

        except NoSuchElementException as e:
            page.tables_and_charts.errors.append('not found any links')
        except TimeoutException as e:
            page.tables_and_charts.errors.append('not found any links')
        except TypeError as e:
            print('exception, xpath is not recognized')
        except Exception as e:
            print('not recognized exception in tables and charts: {}'.format(e))

        # last link check
        try:
            to_all_maps = element.find_element(By.XPATH, ".//div//a[@class='MadadTableMapsToAll']")
            to_all_maps = CbsLink(to_all_maps.get_attribute('href'))
            PageUtility.set_link_status(to_all_maps)
            if not to_all_maps.status_code == 200:
                raise Exception('last link is broken')

        except Exception as e:
            page.tables_and_charts.errors.append('to all charts link is broken')
            print('exception in set_tables_and_charts: {}'.format(e))

    @classmethod
    def check_lines(cls, web_part_lines: [WebPartLine], errors: [str]):
        for web_part_line in web_part_lines:
            link_url = web_part_line.url
            pic_url = web_part_line.pic
            PageUtility.set_link_status(link_url)
            PageUtility.set_link_status(pic_url)
            if not link_url.status_code == 200:
                errors.append('url link is broken')
            if not pic_url.status_code == 200:
                errors.append('image url link is broken')

    @classmethod
    def set_geographic_zone(cls, page: SubjectPage, session: webdriver):
        print('geographic-zone test in: {}'.format(page.name))

        try:
            element: WebElement = session.find_element(By.XPATH, Links.GEOGRAPHIC_ZONE_XPATH.value)
        except NoSuchElementException as e:
            print('no geographic_zone', e)
            return
        except TimeoutException as e:
            print('no geographic_zone', e)
            return
        except TypeError as e:
            print('exception, xpath is not recognized', e)
            return
        except Exception as e:
            print('not recognized exception in geographic_zone', e)
            return
        # check link status
        try:
            a = element.find_element(By.XPATH, './/a').get_attribute('href')
            link = CbsLink(url=a)
            PageUtility.set_link_status(link)
            if not link.status_code == 200:
                page.geographic_zone.errors.append('link is broken')
            else:
                print('link is ok')
            print('status: ', link.status_code)
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

        try:
            main_element = session.find_element(By.XPATH, Links.INTERNATIONAL_COMPARISONS_XPATH.value)
        except NoSuchElementException as e:
            return
        except TimeoutException as e:
            return
        except Exception as e:
            print('not recognized exception in international comparisons', e)
            return

        # check link status
        try:
            main_link = main_element.find_element(by=By.XPATH, value=".//div//a").get_attribute('href')

            link = CbsLink(url=main_link)
            PageUtility.set_link_status(link)
            if not link.status_code == 200:
                page.international_comparisons.errors.append('link is broken')
            else:
                print('link is ok')
            print('status: ', link.status_code)
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
        print('in developing process')

    @classmethod
    def set_pictures_links(cls, page, session):
        print('pictures-links test in: {}'.format(page.name))
        print('in developing process')


class PageUtility:

    @classmethod
    def setPageLevel(cls, root_element, page: SubjectPage):
        # finding the Level inside the page text
        # print('finding span objects...')
        uList = root_element.find_elements_by_xpath(
            "//div[@class='breadcrumb']//span[@class = 'ms-sitemapdirectional']")
        page.level = len(uList) - 2

    @classmethod
    def setPageParent(cls, root_element, page: SubjectPage):
        if page.level is None:
            cls.setPageLevel(root_element, page)
        if page.level > 1:
            uList = root_element.find_elements_by_xpath(
                "//div[@class='breadcrumb']//span[@class = 'ms-sitemapdirectional']//a[@href]")
            page.link = uList[len(uList) - 1].get_attribute('href')
            page.name = uList[len(uList) - 1].text
        # else the parent page is the home page
        else:
            page.link = Links.CBS_HOME_PAGE_HE.value
            page.name = CBS_HOME_PAGE_NAME

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
        try:

            resp = HTTPS.request('GET', link.url,redirect=True)
            link.status_code = resp.status



        except TimeoutException:
            link.status_code = 408
            return
        except URLError as e:
            print('URLError in set_link_status: ', e)
            print('link: ', link.url)
            link.status_code = 404
            return
        except Exception as e:
            print('set link status func unknown exception', e)
            link.status_code = 408
            return

        # case everything went well - still need to check default error page of CBS
        # and link.url.endswith('.aspx')
        if link.status_code == 200 and link.type == 'page':
            # print('inside deep check: ')
            # print(link.url)
            content = resp.data.decode('utf-8')
            # print('content: ', content)
            cls.check_for_cbs_error_page(content, link)
            return

    # gets <a> or <img> web elements and check them for errors
    # returns tuple of list of CBS links from input and list of errors -
    # each error describes the index of the error link
    @classmethod
    def set_url_links(cls, links: [WebElement], attrib='href'):
        link_list = []
        errors = []
        for i, element in enumerate(links):
            url = element.get_attribute(attrib)
            link = CbsLink(url)
            cls.set_link_status(link)
            link_list.append(link)
            if not link.status_code == 200:
                print(str(link.status_code) + str(link.url))
                errors.append(str(i + 1) + 'th link is broken')
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

    @classmethod
    def set_page_lang(cls, page: SubjectPage, root_element):
        try:
            element = root_element.find_element_by_xpath("//a[@id='ctl00_ctl23_lbEnglish']")
        except NoSuchElementException as e:
            print('not a subject page')
            return
        if element.text.upper() == 'ENGLISH':
            page.lang = Language.ENGLISH.value
            return
        page.lang = Language.HEBREW.value

    # @classmethod  # need to be changed according page file_type
    # def set_internal_links(cls, page: SubjectPage, session: webdriver.Chrome):
    #
    #     if page.link.status_code == 200:
    #         # inside links check
    #         try:
    #             session.get(page.link.url)
    #             links = session.find_elements_by_xpath("//div[@class='twoColumn']//a[@href]")
    #             cbs_links = []
    #             for link in links:
    #                 url_: str = link.get_attribute('href')
    #                 text: str = link.text
    #                 if text == '' and url_ == '':
    #                     continue
    #                 else:
    #                     cur_link = CbsLink(url_)
    #                     cur_link.name = text
    #                     cbs_links.append(cur_link)
    #             page.set_inside_links(cbs_links)
    #         except Exception as e:
    #             print('exception was occurred in page: ' + page.name)
    #         finally:
    #             error = False
    #             for link in page:
    #                 if link.status_code == 200:
    #                     error = True
    #                     break
    #         if error:
    #             print(page.name + '::' + 'problems were found')
    #             # need to be replace with inserting errors inside the page
    #             # def wrightToFile(links):
    #         else:
    #             print(page.name + '::' + '200 OK for links inside')

    # @classmethod
    # def set_extra_statistical(cls, page: SubjectPage, root_element:WebDriver):
    #     # check for extra web part - empty statistical (different xPath)
    #     try:
    #         # extra_stats = root_element.find_element_by_xpath(Links.EXTRA_STATS_XPATH.value)
    #         page.stats_part.errors.append('extra web part is showed')
    #         page.isCorrect = False
    #     except TimeoutException:
    #         pass
    #     except NoSuchElementException:
    #         return

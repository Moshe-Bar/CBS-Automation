import requests
from requests.exceptions import InvalidSchema
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from CbsObjects.WebPartLine import WebPartLine
from DataBase.DataBase import Links

from temp.Language import Language

CBS_HOME_PAGE_NAME = 'דף הבית'
CBS_404_TEXTS = ['מתנצלים, הדף לא נמצא', 'Sorry, the page is not found']
CBS_403_TEXTS = ['שלום, אנו מצטערים, הגישה לדף זה נחסמה בשל פעולה לא מורשית', 'Block ID: 5578236093159424155']



class WebPartUtility:
    @classmethod
    def get_web_part(cls,code, session):
        pass
    @classmethod  # need to be changed according page file_type
    def set_internal_links(cls, page: SubjectPage, root_element):
        if page.link.status_code is None:
            PageUtility.set_link_status(page.link)

        if page.link.status_code == 200:
            # inside links check
            try:
                root_element.get(page.link.url)
                links = root_element.find_elements_by_xpath("//div[@class='twoColumn']//a[@href]")
                cbs_links = []
                for link in links:
                    url_: str = link.get_attribute('href')
                    text: str = link.text
                    if text == '' and url_ == '':
                        continue
                    else:
                        cur_link = CbsLink(url_)
                        cur_link.name = text
                        cbs_links.append(cur_link)
                page.set_inside_links(cbs_links)
            except Exception as e:
                print('exception was occurred in page: ' + page.name)
            finally:
                error = False
                for link in page:
                    if link.status_code == 200:
                        error = True
                        break
            if error:
                print(page.name + '::' + 'problems were found')
                # need to be replace with inserting errors inside the page
                # def wrightToFile(links):
            else:
                print(page.name + '::' + '200 OK for links inside')

    @classmethod
    def set_extra_statistical(cls, page: SubjectPage, root_element):
        # check for extra web part - empty statistical (different xPath)
        try:
            extra_stats = root_element.find_element_by_xpath(Links.EXTRA_STATS_XPATH.value)
            page.stats_part.errors.append('extra web part is showed')
            page.isCorrect = False
        except TimeoutException:
            pass
        except NoSuchElementException:
            return

    # only for hebrew page
    @classmethod
    def set_heb_statistical(cls, page: SubjectPage, root_element):
        # assuming the page loaded already - therefore no need to wait

        #   in case the web part is not displayed
        displayed, empty_element = cls.is_element_exist(session=root_element,
                                                        path=Links.HIDDEN_HEBREW_STATS_XPATH.value)
        if displayed:
            return

        try:
            hebrew_stats = root_element.find_element_by_xpath(Links.HEBREW_STATS_XPATH.value)

        except TimeoutException:
            page.stats_part.errors.append("statistical couldn't be found")

            return
        except NoSuchElementException:
            page.stats_part.errors.append("statistical couldn't be found")

            return

        images = hebrew_stats.find_elements_by_xpath(".//ul[@class='cbs-List']//li//img")
        links = hebrew_stats.find_elements_by_xpath(".//ul[@class='cbs-List']//li//a")

        if len(images) == 0 or len(links) == 0:
            page.stats_part.errors.append('images or links content is missing')
        else:
            images, errors = PageUtility.set_url_links(images, attrib='src')
            errors = [error + ' in Statistical image' for error in errors]
            page.stats_part.errors.extend(errors)
            page.stats_part.images.extend(links)

        if len(links) == 0:
            page.stats_part.errors.append('links content is missing')
        else:
            links, errors = PageUtility.set_url_links(links)
            errors = [error + ' ' for error in errors]
            page.stats_part.errors.extend(errors)
            page.stats_part.links.extend(links)

            # *****************************************************************************************************************
        try:
            all_stats_link = root_element.find_element_by_xpath(
                "//div[@id='hebstats']//a[contains(text(),'לכל עלוני הסטטיסטיקל')]")
            cur_link = CbsLink(all_stats_link.get_attribute('href'))
            page.stats_part.links.append(cur_link)
            PageUtility.set_link_status(cur_link)
            if not cur_link.status_code == 200:
                page.stats_part.errors.append('link to all massages is broken')
                page.isCorrect = False
        except NoSuchElementException:
            page.stats_part.errors.append('link to all massages is missing')
            page.isCorrect = False

    @classmethod
    def set_press_releases(cls, page: SubjectPage, session: webdriver.Chrome):

        # when this web part is not displayed the style is "display: none;" and -> text "הודעות לתקשורת"
        # is not exist thus the element wouldn't be found and the function will return
        try:
            element_exist = session.find_element_by_xpath(Links.PRESS_RELEASES_XPATH.value)
            main_element = element_exist.find_element_by_xpath('..')

        except TimeoutException:
            return
        except NoSuchElementException:
            return
        try:
            # title check - not real test because the existent of the web parts is depends on it
            if not main_element.text == 'הודעות לתקשורת':
                page.press_releases.errors.append('title is not correct')

            # inside links check
            dates = main_element.find_elements_by_xpath(".//..//li//div//div[@class= 'pageItemDate']")
            dates = [date.text for date in dates]
            # TODO dates check

            links = main_element.find_elements_by_xpath(".//..//li//div//div[@class= 'pageAll pageItemTitle']//a")
            to_all_massages = main_element.find_element_by_xpath(".//..//a[@class='MadadPressReleasesToAll']")
            if len(links) == 0:
                page.press_releases.errors.append('no content in')
                return
            links.append(to_all_massages)
            links,errors = PageUtility.set_url_links(links)
            page.press_releases.links.extend(links)
            page.press_releases.errors.extend(errors)


        except TimeoutException:
            return
        except NoSuchElementException:
            return

    @classmethod
    def is_element_exist(cls, session: webdriver.chrome, path):
        try:
            element = session.find_element_by_xpath(path)
            if not cls.is_element_displayed(element):
                raise NoSuchElementException
            return (True, element)
        except TimeoutException as e:
            return (False, e.msg)
        except NoSuchElementException as e:
            return (False, e.msg)

    @classmethod
    def is_element_displayed(cls, element):
        if element.get_attribute('style') == 'display: none;':  # display: none;
            return False
        else:
            return True

    @classmethod
    def set_top_box(cls, page: SubjectPage, session: webdriver.Chrome):
        is_exist, main_element = cls.is_element_exist(session, Links.TOP_BOX_XPATH.value)
        # in case the container is displayed
        if is_exist:
            elements = main_element.find_elements_by_xpath(".//div[@class='categoryBox']")
            elements = list(
                map(lambda e: e.find_element_by_xpath(".//a"), filter(lambda x: cls.is_element_displayed(x), elements)))
            # elements = [element.find_element_by_xpath(".//a") for element in elements]

            if len(elements) == 0:  # inside elements are not displayed
                page.top_box.errors.append('top box is displayed without any data')
                return

            else:
                links, errors = PageUtility.set_url_links(elements)
                page.top_box.links.extend(links)
                errors = [error + ' ' for error in errors]
                # errors = list(map(lambda x:x+' in top box',errors))
                page.top_box.errors.extend(errors)
        # element does not found
        else:
            print(main_element + ' ')

    @classmethod
    def set_more_links(cls, page: SubjectPage, root_element):
        # this part on test
        try:
            elem = root_element.find_element_by_xpath(
                "//div[@class='generalBox']//h2[@class='ms-webpart-titleText']//span[contains(text(), 'קישורים נוספים')]")
        except TimeoutException:
            print('element not found')
        finally:
            pass
        # the end

        try:
            part = root_element.find_elements_by_xpath(
                "//div[@class='generalBox']//h2[@class='ms-webpart-titleText']//span[contains(text(), 'קישורים נוספים')]")
            print('num elements found: ', str(len(part)))
            print('found')
        except NoSuchElementException:
            print("the part hasn't been found")
            page.more_links.isHidden = True

    @classmethod
    def set_sub_subjects(cls, page: SubjectPage, session: webdriver.Chrome):
        # find the web part
        try:
            main_element = session.find_element_by_xpath(Links.SUB_SUBJECTS_XPATH.value)
        except NoSuchElementException:
            return
        except TimeoutException:
            return

        # check title
        try:
            title = main_element.find_element_by_xpath("//h2[@class='ms-webpart-titleText']//span").text
            if not title == 'נושאי משנה':
                page.sub_subjects.errors.append('title is not correct')
        except NoSuchElementException:
            page.sub_subjects.errors.append('title is not correct')
        except TimeoutException:
            page.sub_subjects.errors.append('title is not correct')

        # find all the links inside and set their status
        raw_links = main_element.find_elements_by_xpath(".//ul[@class='subtopicsList']//li//a")
        if len(raw_links) == 0:
            page.sub_subjects.errors.append('no internal links')
            return
        internal_links = list(map(lambda li: CbsLink(url=li.get_attribute('href'), page_name=li.text), raw_links))

        for link in internal_links:
            PageUtility.set_link_status(link)
            page.sub_subjects.links.append(link)
            if not link.status_code == 200:
                page.sub_subjects.errors.append('the link: ' + link.name + 'is broken')

    @classmethod
    def set_publications(cls, page: SubjectPage, root_element):
        pass

    @classmethod
    def set_extra_parts(cls, page: SubjectPage, root_element):
        # assuming the page loaded already - therefore no need to wait

        # left side of the page
        try:
            left_extra_parts = root_element.find_element_by_xpath(Links.LEFT_EXTRA_PARTS_XPATH.value)
            page.extra_error_parts.errors.append('left side of the page contains wrong web parts')
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        # right side of the page
        try:
            right_extra_parts = root_element.find_element_by_xpath(Links.RIGHT_EXTRA_PARTS_XPATH.value)
            page.extra_error_parts.errors.append('right side of the page contains wrong web parts')
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        return

    @classmethod
    def set_tools_and_db(cls, page: SubjectPage, session):
        # left side of the page
        try:
            tools_and_db = session.find_element_by_xpath(Links.TOOLS_AND_DB_XPATH.value)
            title = session.find_element_by_xpath("//h2[@id='WpTitleToolAndDataBasesLinks']//span").text
            images = session.find_elements_by_xpath(Links.TOOLS_AND_DB_XPATH.value + "//img")
            links = session.find_elements_by_xpath(Links.TOOLS_AND_DB_XPATH.value + "//a")

            # test image
            if len(images) == 0:
                page.stats_part.errors.append('image content is missing')
                page.isCorrect = False
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
        try:
            # summary = session.find_element_by_xpath(Links.SUMMARY_XPATH.value)
            paragraph = session.find_element_by_xpath(Links.SUMMARY_XPATH.value).text
            images = session.find_elements_by_xpath(Links.SUMMARY_XPATH.value + "//img")
            links = session.find_elements_by_xpath(Links.SUMMARY_XPATH.value + "//a")
            print(paragraph)
            # check text is exist
            if paragraph == '':
                page.summary.errors.append('no text')

            # test images
            if len(images) > 0:
                counter = 0
                for i, img in enumerate(images):
                    print(img.get_attribute('src'))
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
                    print(url.get_attribute('href'))
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
            return
        except Exception as e:
            print('exception in summary test')
            raise e
        return

    @classmethod
    def set_tables_and_charts(cls, page: SubjectPage, session: webdriver):

        try:
            element:WebElement = session.find_element_by_xpath(Links.TABLES_AND_CHARTS_XPATH.value)
        except NoSuchElementException as e:
            return
        except TimeoutException as e:
            return
        except TypeError as e:
            print('exception, xpath is not recognized')
            return
        except Exception:
            print('not recognized exception in tables and charts')
            return

        # title check
        try:

            title = element.find_element_by_xpath(".//h2//span").text
            if not title == 'לוחות ותרשימים':
                page.tables_and_charts.errors.append('title is not correct')
                print(title)

        except NoSuchElementException as e:
            return
        except TimeoutException as e:
            return
        except TypeError as e:
            print('exception, xpath is not recognized')
            return
        except Exception:
            print('not recognized exception in tables and charts')
            return

        # links check
        try:

            li_elements = element.find_elements_by_xpath(".//div//ul//li")
            print('number li: ', len(li_elements))
            web_part_lines = []
            if len(li_elements) == 0:
                raise NoSuchElementException(msg='elements not found')

            for li in li_elements:
                div = li.find_elements_by_xpath(".//div//div")
                pic_url = CbsLink(div[0].find_element_by_xpath(".//a//img").get_attribute('src'))
                link_url = CbsLink(div[0].find_element_by_xpath(".//a").get_attribute('href'))
                name = div[0].text
                date = div[1].text
                web_part_lines.append(WebPartLine(link_url,pic_url,date,name))

            cls.check_lines(web_part_lines,page.tables_and_charts.errors)

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
            to_all_maps = element.find_element_by_xpath(".//div//a[@class='MadadTableMapsToAll']")
            to_all_maps = CbsLink(to_all_maps.get_attribute('href'))
            PageUtility.set_link_status(to_all_maps)
            print(to_all_maps)
            if not to_all_maps.status_code == 200:
                raise Exception('last link is broken')

        except Exception as e:
            page.tables_and_charts.errors.append('to all charts link is broken')
            print('exception in set_tables_and_charts: {}'.format(e))

    @classmethod
    def check_lines(cls,web_part_lines: [WebPartLine], errors: [str]):
        for web_part_line in web_part_lines:
            link_url = web_part_line.url
            pic_url = web_part_line.pic
            PageUtility.set_link_status(link_url)
            PageUtility.set_link_status(pic_url)
            if not link_url.status_code == 200:
                errors.append('url link is broken')
            if not pic_url.status_code == 200:
                errors.append('image url link is broken')

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
            r = requests.get(link.url)
            link.status_code = r.status_code

        except TimeoutException:
            link.status_code = 408
            return
        except InvalidSchema:
            link.status_code = 400
            return

        except ConnectionError as e:
            print('connection error in ' + link.url, e)
            link.status_code = 408
            return


        except Exception as e:
            print('set link status func unknown exception', e)
            link.status_code = 408
            return

        # case everything went well - still need to check default error page of CBS
        # and link.url.endswith('.aspx')
        if link.status_code == 200:
            cls.check_for_cbs_error_page(r.content, link)
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
            PageUtility.set_link_status(link)
            link_list.append(link)
            if not link.status_code == 200:
                print(str(link.status_code) + str(link.url))
                errors.append(str(i + 1) + 'th link is broken')
        return link_list, errors

    @classmethod
    def check_for_cbs_error_page(cls, content, link: CbsLink):
        for error_text in CBS_404_TEXTS:
            if error_text in str(content):
                link.status_code = 404
                return True
        for error_text in CBS_403_TEXTS:
            if error_text in str(content):
                link.status_code = 403
                return True
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
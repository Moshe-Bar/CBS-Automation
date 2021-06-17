import requests
from requests.exceptions import InvalidSchema
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from dataBase.DataBase import Links

from CbsObjects.Language import Language

CBS_HOME_PAGE_NAME = 'דף הבית'
CBS_404_TEXTS = ['מתנצלים, הדף לא נמצא', 'Sorry, the page is not found']
CBS_403_TEXTS = ['שלום, אנו מצטערים, הגישה לדף זה נחסמה בשל פעולה לא מורשית', 'Block ID: 5578236093159424155']


# GUIDE = 'https://www.guru99.com/xpath-selenium.htmls'


class CbsPageUtility:

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
            print('connection error in ' + link.url)
            link.status_code = 408
            return

        # case everything went well - still need to check default error page of CBS
        # and link.url.endswith('.aspx')
        if link.status_code == 200:
            cls.check_for_cbs_error_page(r.content, link)
            return

    @classmethod  # need to be changed according page type
    def set_internal_links(cls, page: SubjectPage, root_element):
        if page.link.status_code is None:
            cls.set_link_status(page.link)

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
    def create_pages(cls, link_list):
        return [SubjectPage(link, link.name) for link in link_list]

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

    @classmethod
    def set_extra_statistical(cls, page: SubjectPage, root_element):
        # check for extra web part - empty statistical (different xPath)
        try:
            extra_stats = root_element.find_element_by_xpath(Links.EXTRA_STATS_XPATH.value)
            page.stats_part.errors.append('error: statistical - extra web part is showed')
            page.isCorrect = False
        except TimeoutException:
            pass
        except NoSuchElementException:
            return

    # only for hebrew page
    @classmethod
    def set_heb_statistical(cls, page: SubjectPage, root_element):
        # assuming the page loaded already - therefore no need to wait

        # empty extra web part is not exist 200
        # *****************************************************************************************************************

        # in case stats is hidden there is nothing to check

        try:
            # root_element.implicitly_wait(1)
            hidden_stats = WebDriverWait(root_element, 0.5).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, Links.HIDDEN_HEBREW_STATS_XPATH.value)))
            print('not exception')
            # hidden_stats = root_element.find_element_by_xpath(Links.HIDDEN_HEBREW_STATS.value)
            page.stats_part.isHidden = True
            return
        except TimeoutException:
            print('timout')
        except NoSuchElementException:
            print('no element')

        #   in case the web part is showed need to  be check (it displayed)
        try:
            hebrew_stats = root_element.find_element_by_xpath(Links.HEBREW_STATS_XPATH.value)

        except TimeoutException:
            page.stats_part.errors.append("statistical couldn't be found")
            page.isCorrect = False
            return
        except NoSuchElementException:
            page.stats_part.errors.append("statistical couldn't be found")
            page.isCorrect = False
            return

        page.stats_part.isHidden = False
        s_pages_images = hebrew_stats.find_elements_by_xpath("//ul[@class='cbs-List']//li//img")
        s_pages_links = hebrew_stats.find_elements_by_xpath("//ul[@class='cbs-List']//li//a")

        if len(s_pages_images) == 0 or len(s_pages_links) == 0:
            page.stats_part.errors.append('images or links content is missing in Statistical')
            page.isCorrect = False
        else:
            for i, img in enumerate(s_pages_images):
                cur_link = CbsLink(img.get_attribute('src'))
                CbsPageUtility.set_link_status(cur_link)
                page.stats_part.images.append(cur_link)
                if not cur_link.status_code == 200:
                    page.stats_part.errors.append('image is broken in Statistical')
                    page.isCorrect = False
            if len(s_pages_links) == 0:
                page.stats_part.errors.append('links content is missing in Statistical')
                page.isCorrect = False
            else:
                for i, sheet in enumerate(s_pages_links):
                    cur_link = CbsLink(sheet.get_attribute('href'))
                    page.stats_part.images.append(cur_link)
                    CbsPageUtility.set_link_status(cur_link)
                    if not cur_link.status_code == 200:
                        page.stats_part.errors.append('link is broken in Statistical')
                        page.isCorrect = False

            # *****************************************************************************************************************
            try:
                all_stats_link = root_element.find_element_by_xpath(
                    "//div[@id='hebstats']//a[contains(text(),'לכל עלוני הסטטיסטיקל')]")
                cur_link = CbsLink(all_stats_link.get_attribute('href'))
                page.stats_part.links.append(cur_link)
                CbsPageUtility.set_link_status(cur_link)
                if not cur_link.status_code == 200:
                    page.stats_part.errors.append('link to all massages is broken in Statistical')
                    page.isCorrect = False
            except NoSuchElementException:
                page.stats_part.errors.append('link to all massages is missing in Statistical')
                page.isCorrect = False

    @classmethod
    def set_press_releases(cls, page: SubjectPage, root_element):
        # check for extra web part - empty press releases (different xPath)
        try:
            extra_p_releases = root_element.find_element_by_xpath(Links.EXTRA_PREALESES_XPATH.value)
            page.press_releases.errors.append('extra press_releases is showing up')
            page.isCorrect = False
        except TimeoutException:
            pass
        except NoSuchElementException:
            return

    @classmethod
    def set_top_box(cls, page: SubjectPage, session: webdriver.Chrome):
        pass

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
    def set_sub_subjects(cls, page: SubjectPage, root_element):
        # TODO
        # need to put the level first
        # cls.setPageLevel(page=page, open_session= session)

        # find the web part
        try:
            part = root_element.find_element_by_xpath(Links.SUB_SUBJECTS_XPATH.value)
        except NoSuchElementException:
            page.sub_subjects.isHidden = True
            return

        # check title
        try:
            title = part.find_element_by_xpath("//h2[@class='ms-webpart-titleText']//span").text
            if not title == 'נושאי משנה':
                page.sub_subjects.errors.append('title is not correct')
                page.isCorrect = False
        except NoSuchElementException:
            page.sub_subjects.errors.append('title is not correct')
            page.isCorrect = False

        # find all the links inside and set their status
        raw_links = part.find_elements_by_xpath("//ul[@class='subtopicsList']//li//a")
        if len(raw_links) == 0:
            page.sub_subjects.errors.append('no internal links while web part is visible')
            page.isCorrect = False
        internal_links = [CbsLink(url=li.get_attribute('href'), page_name=li.text) for li in raw_links]
        page.sub_subjects.links = internal_links
        for link in internal_links:
            # TODO async as must
            CbsPageUtility.set_link_status(link)
            if not link.status_code == 200:
                page.sub_subjects.errors.append('the link: ' + link.name + 'is broken')
                page.isCorrect = False

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
    def set_tools_and_db(cls, page: SubjectPage, root_element):
        # left side of the page
        try:
            tools_and_db = root_element.find_element_by_xpath(Links.TOOLS_AND_DB_XPATH.value)
            title = root_element.find_element_by_xpath("//h2[@id='WpTitleToolAndDataBasesLinks']//span").text
            images = root_element.find_elements_by_xpath(Links.TOOLS_AND_DB_XPATH.value + "//img")
            links = root_element.find_elements_by_xpath(Links.TOOLS_AND_DB_XPATH.value + "//a")

            # test image
            if len(images) == 0:
                page.stats_part.errors.append('image content is missing in tools and DB')
                page.isCorrect = False
            else:
                for i, img in enumerate(images):
                    cur_link = CbsLink(img.get_attribute('src'))
                    CbsPageUtility.set_link_status(cur_link)
                    page.tools_and_db.images.append(cur_link)
                    if not cur_link.status_code == 200:
                        page.tools_and_db.errors.append('image is broken in tools and DB')
                        page.isCorrect = False

            # test links
            if len(links) == 0:
                page.stats_part.errors.append('link content is missing in tools and DB')
                page.isCorrect = False
            else:
                for i, sheet in enumerate(links):
                    cur_link = CbsLink(sheet.get_attribute('href'))
                    page.tools_and_db.links.append(cur_link)
                    CbsPageUtility.set_link_status(cur_link)
                    if not cur_link.status_code == 200:
                        page.tools_and_db.errors.append('link is broken in tools and DB')
                        page.isCorrect = False

            # test title
            if not title == 'כלים ומאגרי נתונים':
                print(title)
                page.tools_and_db.errors.append('tools and DB: title i not correct')
                print('tools and DB: title i not correct')

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
            summary = session.find_element_by_xpath(Links.SUMMARY_XPATH.value)
            text = session.find_element_by_xpath(Links.SUMMARY_XPATH.value + "//p").text
            images = session.find_elements_by_xpath(Links.SUMMARY_XPATH.value + "//img")
            links = session.find_elements_by_xpath(Links.SUMMARY_XPATH.value + "//a")

            # check text is exist
            if text == '':
                page.summary.errors.append('no text in summary')

            # test images
            if len(images) > 0:
                counter = 0
                print(str(len(images)) + ' images')
                for i, img in enumerate(images):
                    print(img.get_attribute('src'))
                    cur_link = CbsLink(img.get_attribute('src'))
                    CbsPageUtility.set_link_status(cur_link)
                    page.summary.images.append(cur_link)
                    if not cur_link.status_code == 200:
                        counter += 1

                if counter > 1:
                    page.summary.errors.append('{} images are broken in summary'.format(counter))
                elif counter == 1:
                    page.summary.errors.append('{} image is broken in summary'.format(counter))

            # test links
            if len(links) > 0:
                counter = 0
                print(str(len(links)) + ' links')
                for i, url in enumerate(links):
                    print(url.get_attribute('href'))
                    cur_link = CbsLink(url.get_attribute('href'))
                    page.summary.links.append(cur_link)
                    CbsPageUtility.set_link_status(cur_link)
                    if not cur_link.status_code == 200:
                        counter += 1

                if counter > 1:
                    page.summary.errors.append('{} links is broken in summary'.format(counter))
                elif counter == 1:
                    page.summary.errors.append('{} link is broken in summary'.format(counter))

        except TimeoutException:
            pass
        except NoSuchElementException:
            print("summary couldn't be found")
            return
        except Exception as e:
            print('exception in summary test')
            raise e
        return

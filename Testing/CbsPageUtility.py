import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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
        except TimeoutException:
            link.status_code = 408
            return
        except ConnectionError as e:
            print('connection error in ' + link.url)
            link.status_code = 408
            return
        # case everything went well - still need to check default error page of CBS
        if r.status_code == 200 and link.url.endswith('.aspx'):
            cls.check_for_cbs_error_page(r.content, link)
        link.status_code = r.status_code

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
                print('exception was occured in page: ' + page.name)
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
                return
        for error_text in CBS_403_TEXTS:
            if error_text in str(content):
                link.status_code = 403
                return

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
            hidden_stats = root_element.find_element_by_xpath(Links.HIDDEN_HEBREW_STATS.value)
            page.stats_part.isHidden = True
            return
        except TimeoutException:
            pass
        except NoSuchElementException:
            pass

        #   in case the web part is showed need to  be check (it displayed)
        try:
            hebrew_stats = root_element.find_element_by_xpath(Links.HEBREW_STATS.value)

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
    def set_top_box(cls, page: SubjectPage, session: webdriver.Chrome):
        pass

    @classmethod
    def set_more_links(cls, page: SubjectPage, root_element):
        # this part on test
        try:
            elem = root_element.find_element_by_xpath("//div[@class='generalBox']//h2[@class='ms-webpart-titleText']//span[contains(text(), 'קישורים נוספים')]")
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
    def set_tools_and_database(cls, page: SubjectPage, root_element):
        pass

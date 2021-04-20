import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

from CbsClasses.CbsLink import CbsLink
from CbsClasses.CbsPage import CbsPage
from LinksUtility.usefulLinks import Links

from CbsClasses.Language import Language

CBS_HOME_PAGE_NAME = 'דף הבית'
CBS_404_TEXTS = ['מתנצלים, הדף לא נמצא', 'Sorry, the page is not found']
CBS_403_TEXTS = ['שלום, אנו מצטערים, הגישה לדף זה נחסמה בשל פעולה לא מורשית', 'Block ID: 5578236093159424155']


# GUIDE = 'https://www.guru99.com/xpath-selenium.htmls'


class CbsPageUtility:

    @classmethod
    def setPageLevel(cls, open_session, page: CbsPage):
        # finding the Level inside the page text
        # print('finding span objects...')
        uList = open_session.find_elements_by_xpath(
            "//div[@class='breadcrumb']//span[@class = 'ms-sitemapdirectional']")
        page.level = len(uList) - 2

    @classmethod
    def setPageParent(cls, open_session, page: CbsPage):
        if page.level is None:
            cls.setPageLevel(open_session, page)
        if page.level > 1:
            uList = open_session.find_elements_by_xpath(
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
            pages.append(CbsPage(link[0], link[1]))
        return pages

    @classmethod
    def create_web_driver(cls, wait_time=10):
        try:
            driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
            driver.implicitly_wait(wait_time)
            return driver
        except WebDriverException as e:
            print('driver error: ' + str(e))

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
    def set_internal_links(cls, page: CbsPage, open_session: webdriver.Chrome):
        if page.link.status_code is None:
            cls.set_link_status(page.link)

        if page.link.status_code == 200:
            # inside links check
            try:
                open_session.get(page.link.url)
                links = open_session.find_elements_by_xpath("//div[@class='twoColumn']//a[@href]")
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
        return [CbsPage(link, link.name) for link in link_list]

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
    def set_page_lang(cls, page: CbsPage, session: webdriver.Chrome):
        try:
            element = session.find_element_by_xpath("//a[@id='ctl00_ctl23_lbEnglish']")
        except NoSuchElementException as e:
            print('not a subject page')
            return
        if element.text.upper() == 'ENGLISH':
            page.lang = Language.ENGLISH.value
            return
        page.lang = Language.HEBREW.value

    @classmethod
    # only for hebrew page
    def set_MomentOfStatistics_part(cls,page: CbsPage, session: webdriver.Chrome):
        # assuming the page loaded already - therefore no need to wait
        session.implicitly_wait(2)
        # *****************************************************************************************************************
        # check for extra web part - empty statistical (different xPath)
        try:
            session.find_element_by_xpath("//div[@id='MSOZoneCell_WebPartWPQ13']")
            page.stats_part.errors.append('error: statistical - extra web part')
        except  NoSuchElementException:
            # empty extra web part is not exist 200
            pass
        # *****************************************************************************************************************
        try:
            # in case stats is hidden there is nothing to check
            session.find_element_by_xpath("//div[@id='hebstats']//div[@style='display:none']")
            page.stats_part.isHidden = True

            return
        except NoSuchElementException:
            #   in case the web part is showed need to  be check (it displayed)
            page.stats_part.isHidden = False
            s_pages_images = session.find_elements_by_xpath("//div[@id='hebstats']//ul[@class='cbs-List']//li//img")
            s_pages_links = session.find_elements_by_xpath("//div[@id='hebstats']//ul[@class='cbs-List']//li//a")
            if len(s_pages_images) == 0:
                page.stats_part.errors.append('images content is missing in Statistical')
            else:
                for i, img in enumerate(s_pages_images):
                    cur_link = CbsLink(img.get_attribute('src'))
                    CbsPageUtility.set_link_status(cur_link)
                    page.stats_part.images.append(cur_link)
                    if not cur_link.status_code == 200:
                        page.stats_part.errors.append('image is broken in Statistical')
            if len(s_pages_links) == 0:
                page.stats_part.errors.append('links content is missing in Statistical')
            else:
                for i, sheet in enumerate(s_pages_links):
                    cur_link = CbsLink(sheet.get_attribute('href'))
                    page.stats_part.images.append(cur_link)
                    CbsPageUtility.set_link_status(cur_link)
                    if not cur_link.status_code == 200:
                        page.stats_part.errors.append('link is broken in Statistical')
        # *****************************************************************************************************************
        try:
            all_stats_link = session.find_element_by_xpath(
                "//div[@id='hebstats']//a[contains(text(),'לכל עלוני הסטטיסטיקל')]")
            cur_link = CbsLink(all_stats_link.get_attribute('href'))
            page.stats_part.links.append(cur_link)
            CbsPageUtility.set_link_status(cur_link)
            if not cur_link.status_code == 200:
                page.stats_part.errors.append('link to all massages is broken in Statistical')
        except NoSuchElementException:
            page.stats_part.errors.append('link to all massages is missing in Statistical')
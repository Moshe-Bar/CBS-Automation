from CbsClasses.CbsLink import CbsLink
from CbsClasses.CbsPage import CbsPage

import sys

from enum import Enum


class DataBase:
    @classmethod
    def get_CBS_links(cls):
        links = []
        try:
            with open(r'D:\Current\Selenium\NewAutomationEnv\dataBase\heb_pages_links.txt', 'r') as f:
                for line in f:
                    li = line.split()
                    cbs_link = CbsLink(li[0])
                    cbs_link.name = ' '.join(li[1:])
                    links.append(cbs_link)
                f.close()
        except Exception as e:
            print('database file did not read', e)
            return None
        return links

    @classmethod
    def get_CBS_pages(cls):
        links = cls.get_CBS_links()  # the links only saved locally
        pages = [CbsPage(link, link.name) for link in links]
        return pages

    # @classmethod
    # def get_cbs_pages_online(cls):
    #     driver = TestUtility.get_sessions()[0]  # returns a one obj list with defualt driver
    #     driver.get(Links.CBS_MAP_SITE_HE.value) # opens the map site for extracting the links inside
    #     raw_urls = driver.find_elements_by_xpath(Links.MAP_LINKS_XPATH)
    #     print('number of link objects found: ', len(raw_urls))
    #     pages = list(map(lambda x: CbsPage(CbsLink(x.get_attribute('href')), x.text), raw_urls))
    #     driver.close()
    #     return pages


class Links(Enum):
    CBS_HOME_PAGE_HE = 'https://www.cbs.gov.il/he/Pages/default.aspx'
    CBS_MAP_SITE_HE = 'https://www.cbs.gov.il/he/pages/sitemap.aspx'
    CBS_MAP_SITE_EN = 'https://www.cbs.gov.il/en/Pages/sitemap.aspx'
    ROOT_DIR = sys.path[1]
    CHROME_DRIVER = ROOT_DIR + "\chromedriver.exe"
    MAP_LINKS_XPATH = "//ul[@class='level1 sitemapmenu']//li[@class='ng-scope']//ul[@class='level2']//li[@class='ng-scope']//ul[@class='level3']//li//a"
    SUB_SUBJECTS_XPATH = "//div[@class='generalBox ng-scope'][@ng-controller='subSubjectsList']"
# driver = TestUtility.get_sessions()[0]
# driver.get('https://getsharex.com/')

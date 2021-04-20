import time

import requests

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from CbsClasses.CbsLink import CbsLink
from CbsClasses.CbsPage import CbsPage

from LinksUtility.usefulLinks import Links

# GUIDE = 'https://www.guru99.com/xpath-selenium.htmls'


class CbsPageUtility:

    @classmethod
    def findPageLevel(cls, page_source):
        # finding the Level inside the page text
        # print('finding span objects...')
        uList = page_source.find_elements_by_xpath(
            "//div[@class='breadcrumb']//span[@class='breadcrumbPathSeparator']")
        return len(uList) - 1

    @classmethod
    def findPageParent(cls, page_source):
        uList = page_source.find_elements_by_xpath(
            "//div[@class='breadcrumb']//span[@class='breadcrumbPathSeparator']")
        return uList[len(uList) - 2]

    @classmethod
    def create_pages(cls, link_list):
        pages = []
        for link in link_list:
            pages.append(CbsPage(link[0], link[1]))
        return pages

    @classmethod
    def create_web_driver(cls, wait_time=10):
        driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
        driver.implicitly_wait(wait_time)
        return driver

    @classmethod
    def checkLink(cls, link: CbsLink):
        try:
            r = requests.get(link.link)
        except TimeoutException:
            link.status_code = 408
            return
            # case everything went well
        link.status_code = r.status_code

    def wrightToFile(links):
        with open('log.txt', 'wb') as logFile:
            for link in links:
                logFile.write(link, '\n')
            logFile.close()

    def getWPGeneralBoxtoplinks(driver):
        gb = driver.find_elements_by_xpath(
            "//div[@class='generalBox top-LinksUtility']//div[not(contains(@style, 'display: none;'))]//a")
        return gb

    def saveHtmlFile(driver):
        with open("/path/to/page_source.html", "w") as f:
            f.write(driver.page_source)
            f.close()
            return "/path/to/page_source.html"

    def getWPToolsAndDatabases(driver):
        pass

    def getWPExternalLinks(driver):
        pass

    def getWpStatistical(driver, lang):
        if lang == 'HE':
            images = driver.find_elements_by_xpath(
                "//div[@id='hebstats']//img")

        # lang == 'EN' :
        else:
            images = driver.find_elements_by_xpath(
                "//div[@id='engstats']//img")

            pass

    def testGetFromSELObj(driver):
        divs = driver.find_elements_by_xpath(
            "//div[@class='generalBox top-LinksUtility']//div[not(contains(@style, 'display: none;'))]")
        # find_elements_by_xpath("a")
        ord = []
        for div in divs:
            a = div.find_element_by_xpath("a")
            link = a.get_attribute('href')
            ord.append((a.text[::-1], link))
        print(ord, '\n')

    def checkChildPage(driver):
        driver.get(URL)
        time.sleep(8)
        link = driver.find_element_by_xpath(
            "//div[@class='categoryBox comparisons-wrapper ng-binding']//a").get_attribute('href')
        driver.get(link)
        time.sleep(8)
        if len(list(driver.find_elements_by_xpath("//div[@id='NoResult']"))) == 1:
            print('error in WebPart')

# def Main():
#     # initial selenium driver
#     driver = webdriver.Chrome(DRIVER_PATH)
#     # driver.get(URL)
#     # level = getLevel(driver)
#     # generalWP = getWPGeneralBoxtoplinks(driver)
#     # LinksUtility = list(map(lambda x: x.get_attribute('href'), generalWP))
#
#     # print('level of page : ', level)
#     # print('number of general box items : ', len(list(generalWP)))
#
#     print('test...')
#     CbsPageUtility.checkChildPage(driver)
#     driver.close()
#     # for english site '[::-1]' need to be deleteted
#     # link_list = list(
#     #     map(lambda x: (x.get_attribute('href'), x.text[::-1]), raw_list))
#     # broken_links = []
#
#     # checking the LinksUtility
#     # for link in link_list:
#     #     try:
#     #         r = requests.head(link[0])
#     #     except Exception as e:
#     #         broken_links.append((link, 'code :', e))
#
#     #         continue
#     #     if(not r.status_code == 200):
#     #         broken_links.append((link, 'code :', r.status_code))
#     #     print(link[1], r.status_code)
#
#     # number of broken LinksUtility
#     # print('broken LinksUtility: ', len(broken_links))
#     # for link in broken_links:
#     #     print(link)
#     # wrightToFile()
#
#
# if __name__ == "__main__":
#     Main()

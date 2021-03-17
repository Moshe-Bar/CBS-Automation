from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from CbsPage import CbsPage
import time


DRIVER_PATH = 'C:\chromedriver.exe'
URL = r'https://www.cbs.gov.il/he/subjects/Pages/%D7%A7%D7%A9%D7%99%D7%A9%D7%99%D7%9D.aspx'
GUIDE = 'https://www.guru99.com/xpath-selenium.htmls'
CHILD_PAGE = r'https://www.cbs.gov.il/he/Pages/search/searchResultsInternationalComparisons.aspx?subject=%D7%90%D7%96%D7%A8%D7%97%D7%99%D7%9D%20%D7%95%D7%AA%D7%99%D7%A7%D7%99%D7%9D#Default=%7B%22k%22%3A%22%22%2C%22r%22%3A%5B%7B%22n%22%3A%22owstaxIdCbsMMDSubjects%22%2C%22t%22%3A%5B%22string(%5C%22%230ce5125a3-580a-46ed-8777-433d3fa105b3%5C%22)%22%5D%2C%22o%22%3A%22and%22%2C%22k%22%3Afalse%2C%22m%22%3Anull%7D%5D%7D#479c7939-cdc1-4078-a8aa-3699526df1e6=%7B%22k%22%3A%22%22%2C%22r%22%3A%5B%7B%22n%22%3A%22owstaxIdCbsMMDSubjects%22%2C%22t%22%3A%5B%22string(%5C%22%230ce5125a3-580a-46ed-8777-433d3fa105b3%5C%22)%22%5D%2C%22o%22%3A%22and%22%2C%22k%22%3Afalse%2C%22m%22%3Anull%7D%5D%7D'


def wrightToFile(links):
    with open('log.txt', 'wb') as logFile:
        for link in links:
            logFile.write(link, '\n')
        logFile.close()


def getLevel(driver):
    # finding the links in the page
    print('finding span objects...')
    uList = driver.find_elements_by_xpath(
        "//div[@class='breadcrumb']//span[@class='breadcrumbPathSeparator']")
    return len(uList) - 1


def saveHtmlFile(driver):
    with open("/path/to/page_source.html", "w") as f:
        f.write(driver.page_source)
        f.close()
        return "/path/to/page_source.html"


def getWPToolsAndDatabases(driver):
    pass


def getWPExternalLinks(driver):
    pass


def getWPGeneralBoxtoplinks(driver):
    gb = driver.find_elements_by_xpath(
        "//div[@class='generalBox top-links']//div[not(contains(@style, 'display: none;'))]//a")
    return gb


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
        "//div[@class='generalBox top-links']//div[not(contains(@style, 'display: none;'))]")
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


def Main():
    # initial selenium driver
    driver = webdriver.Chrome(DRIVER_PATH)
    # driver.get(URL)
    # level = getLevel(driver)
    # generalWP = getWPGeneralBoxtoplinks(driver)
    # links = list(map(lambda x: x.get_attribute('href'), generalWP))

    # print('level of page : ', level)
    # print('number of general box items : ', len(list(generalWP)))

    print('test...')
    checkChildPage(driver)
    driver.close()
    # for english site '[::-1]' need to be deleteted
    # link_list = list(
    #     map(lambda x: (x.get_attribute('href'), x.text[::-1]), raw_list))
    # broken_links = []

    # checking the links
    # for link in link_list:
    #     try:
    #         r = requests.head(link[0])
    #     except Exception as e:
    #         broken_links.append((link, 'code :', e))

    #         continue
    #     if(not r.status_code == 200):
    #         broken_links.append((link, 'code :', r.status_code))
    #     print(link[1], r.status_code)

    # number of broken links
    # print('broken links: ', len(broken_links))
    # for link in broken_links:
    #     print(link)
    # wrightToFile()


if __name__ == "__main__":
    Main()

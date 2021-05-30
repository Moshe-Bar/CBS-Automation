import time
from selenium import webdriver

import requests

from CbsObjects.Pages.SubjectPage import SubjectPage
from DataBase import Links


def wrightToFile(links):
    with open('log.txt', 'wb') as logFile:
        for link in links:
            logFile.write(link, '\n')
        logFile.close()


def getCurrentLinks(driver):
    # finding the LinksUtility in the page
    print('finding all HREF objects...')
    uList = driver.find_elements_by_xpath(
        "//ul[@class='level1 sitemapmenu']//li[@class='ng-scope']//ul[@class='level2']//li[@class='ng-scope']//ul["
        "@class='level3']//li//a")
    # uList = driver.find_elements_by_xpath("//a[@href]")
    print('uList size: ' + str(len(uList)))
    return uList


def testLinks(link_list, broken_links):
    for link in link_list:
        try:
            r = requests.head(link[0])
        except Exception as e:
            broken_links.append((link, 'code :', e))

            continue
        if not r.status_code == 200:
            broken_links.append((link, 'code :', r.status_code))
        print(link[1], r.status_code)


def create_pages(link_list):
    pages = []
    for link in link_list:
        pages.append(SubjectPage(link[0], link[1]))
    return pages


def main():
    start_time = time.time()
    # initial selenium driver
    driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
    driver.get(Links.CBS_MAP_SITE_HE.value)
    raw_list = getCurrentLinks(driver)

    # arranging the LinksUtility in an appropriate list
    print('number of cbs_link objects found : ', len(raw_list))
    # for english site '[::-1]' need to be deleteted
    link_list = list(
        map(lambda x: (x.get_attribute('href'), x.text), raw_list))
    broken_links = []
    # generate pages
    pages = create_pages(link_list)
    # checking the LinksUtility synchronically
    testLinks(link_list, broken_links)

    # number of broken LinksUtility
    print('broken LinksUtility: ', len(broken_links))
    for link in broken_links:
        print(link)
    # wrightToFile()

    # l_list = list(
    #     map(lambda x: x.get_attribute('href'), raw_list))
    # print('start testing with grequests')
    # rs = (grequests.get(u) for u in l_list)
    # grequests.map(rs)
    driver.close()
    print(str(time.time() - start_time))


if __name__ == "__main__":
    main()

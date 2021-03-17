from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
# from ....te. import AsyncRequests
# from CBS_Automation.UI.window import MainWindow
# import tkinter as tk


HOME_PAGE_URL = 'https://www.cbs.gov.il/he/Pages/default.aspx'
MAP_SITE_URL = 'https://www.cbs.gov.il/he/pages/sitemap.aspx'
ENGLISH_MAP_SITE_URL = 'https://www.cbs.gov.il/en/Pages/sitemap.aspx'
DRIVER_PATH = 'C:\chromedriver.exe'


def wrightToFile(links):
    with open('log.txt', 'wb') as logFile:
        for link in links:
            logFile.write(link,'\n')
        logFile.close()


def getCurrentLinks(driver):
    # finding the links in the page 
    print('finding all HREF objects...')
    uList = driver.find_elements_by_xpath(
        "//ul[@class='level1 sitemapmenu']//li[@class='ng-scope']//ul[@class='level2']//li[@class='ng-scope']//ul[@class='level3']//li//a")
    return uList


def Main():
    # initial selenium driver
    driver = webdriver.Chrome(DRIVER_PATH)
    driver.get(MAP_SITE_URL)
    raw_list = getCurrentLinks(driver)
  

    print('number of li objects found : ', len(raw_list))
    # for english site '[::-1]' need to be deleteted
    link_list = list(
        map(lambda x: (x.get_attribute('href'), x.text[::-1]), raw_list))
    broken_links = []

    test = AsyncRequests(link_list)
    test.asyncC()
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
    driver.close()

if __name__ == "__main__":
    Main()

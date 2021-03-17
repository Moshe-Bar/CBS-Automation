from tkinter import mainloop
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import thread
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


def checkLinks(links):
    link_list_info=[]
    for link in links:
        try:
            r = requests.head(link[0])
        except Exception as e:
            link_list_info.append((link, 'Exception :', e.text))
            print(link[1], 'Exception : ', e.text)
            continue

        link_list_info.append((link, 'code :', r.status_code))
        print(link[1], r.status_code)

    return link_list_info

def Main():
    # initial selenium driver
    driver = webdriver.Chrome(DRIVER_PATH)
    driver.get(MAP_SITE_URL)
    raw_list = getCurrentLinks(driver)
    

    print('number of li objects found : ', len(raw_list))

    link_list = list(
        map(lambda x: (x.get_attribute('href'), x.text[::-1]), raw_list))
    checkLinks(link_list)
    # [print(i.text[::-1]) for i in raw_list]

    

    try:
        thread.start_new_thread( checkLinks, ("Thread-1", 2, ) )
        thread.start_new_thread( checkLinks, ("Thread-2", 4, ) )
    except:
        print("Error: unable to start thread") 

    driver.close()
    # while 1:
    #     pass

if __name__ == "__main__":
    Main()
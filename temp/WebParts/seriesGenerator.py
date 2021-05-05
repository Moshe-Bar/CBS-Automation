from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


# from CBS_Automation.UI.window import MainWindow
# import tkinter as tk


HOME_PAGE_URL = 'https://www.cbs.gov.il/he/Pages/default.aspx'
MAP_SITE_URL = 'https://www.cbs.gov.il/he/pages/sitemap.aspx'
ENGLISH_MAP_SITE_URL = 'https://www.cbs.gov.il/en/Pages/sitemap.aspx'
DRIVER_PATH = 'C:\chromedriver.exe'
SOME_PAGE = r'https://www.cbs.gov.il/he/subjects/Pages/%D7%93%D7%95%D7%97-%D7%9E%D7%A1-9-%D7%91%D7%A0%D7%99-55-%D7%95%D7%9E%D7%A2%D7%9C%D7%94.aspx'


def wrightToFile(links):
    with open('log.txt', 'wb') as logFile:
        for link in links:
            logFile.write(link, '\n')
        logFile.close()


def getCurrentLinks(driver):
    driver.get(MAP_SITE_URL)
    # finding the LinksUtility in the page
    print('finding all HREF objects...')
    try:
        uList = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='level1 sitemapmenu']//cbs_link[@class='ng-scope']//ul[@class='level2']//cbs_link[@class='ng-scope']//ul[@class='level3']//cbs_link//a")))
        print("mapsite is ready!")
    except TimeoutException:
        print("Loading mapsite took too much time!")
        return
    # uList = driver.find_elements_by_xpath(
    #     "//ul[@class='level1 sitemapmenu']//cbs_link[@class='ng-scope']//ul[@class='level2']//cbs_link[@class='ng-scope']//ul[@class='level3']//cbs_link//a")
    print('number of cbs_link objects found : ', len(uList))
    # for english site '[::-1]' need to be deleteted
    link_list = list(
        map(lambda x: (x.get_attribute('href'), x.text[::-1]), uList))
    return link_list


def generatorTest(driver, link, name, errors_array):
    print('finding generator web part...')
    driver.get(link)

    try:
        generator = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='categoryBox statisticsBox']//div//a")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
        errors_array.append((link, name))
        return
    except NoSuchElementException:
        print("Element did not found")
        return
    generator_link = generator.get_attribute('href')

    if(generator_link == 'javascript:void(0)'):
        errors_array.append((link, name))
        print('invalid link')
        return
    try:
        r = requests.head(generator_link)
    except Exception as e:
        errors_array.append((link, name))
        return
    if(not r.status_code == 200):
        errors_array.append((link, name))
        return
    # work well
    print('work well')
    return


def Main():
    # initial selenium driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # options.add_argument('--window-size=1920x1080')
    # options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(DRIVER_PATH)

    link_list = getCurrentLinks(driver)

    errors_array = []
    for link in link_list:
        generatorTest(driver, link[0], link[1], errors_array)

    for error in errors_array:
        print(error[1], error[0], '\n')

    driver.close()
    driver.quit()
    # for link in link_list:
    #     print(link[0])

    # checking the LinksUtility
    # for link in link_list:
    #     try:
    #         r = requests.head(link[0])
    #     except Exception as e:
    #         broken_links.append((link, 'code :', e))

    #         continue
    #     if(not r.status_code == 200):
    #         broken_links.append((link, 'code :', r.status_code))
    #     print(link[1], r.status_code)

    # number of broken LinksUtility
    # print('broken LinksUtility: ', len(broken_links))
    # for link in broken_links:
    #     print(link)
    # wrightToFile()
if __name__ == "__main__":
    Main()

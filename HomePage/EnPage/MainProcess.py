from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

URL = 'https://www.cbs.gov.il/en/Pages/default.aspx'
DRIVER_PATH = 'C:\chromedriver.exe'


def getCurrentLinks(driver):
    driver.get(URL)
    return driver.find_elements_by_tag_name('a')
    
def connectivityCheck():
    pass

driver = webdriver.Chrome(DRIVER_PATH)
raw_list = getCurrentLinks(driver=driver)
print('len of raw list : ', len(raw_list))
arrangedList =  list(
        map(lambda x: (x.get_attribute('href'), x.text), raw_list))
print('arrangedList : ',arrangedList[0])
for link in arrangedList:
    print(link[0])       

driver.close()
from selenium import webdriver

import CbsPageUtility
from LinksUtility.usefulLinks import Links

page = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%9C%D7%A4%D7%99-%D7%93%D7%AA-%D7%95%D7%A7%D7%91%D7%95%D7%A6%D7%AA-%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94.aspx'


def findPageParent(page_source):
    uList = page_source.find_elements_by_xpath(
        "//div[@class='breadcrumb']//span")
    print(uList[len(uList) - 2].text)


driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
driver.implicitly_wait(10) # seconds
driver.get(page)
findPageParent(driver)
# driver.close()

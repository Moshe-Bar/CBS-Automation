from selenium.common.exceptions import TimeoutException, NoSuchElementException

from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from Testing.CbsPageUtility import CbsPageUtility
from Testing.TestUtility import TestUtility
from dataBase.DataBase import Links

URL1 = r'https://www.cbs.gov.il/he/subjects/Pages/%D7%94%D7%A8%D7%99%D7%95%D7%A0%D7%95%D7%AA-%D7%99%D7%93%D7%95%D7%A2%D7%99%D7%9D.aspx'



page1 = SubjectPage(CbsLink(URL1) ,'בריאות מקומי')
session1 = TestUtility.create_web_driver()
session1.get(page1.link.url)

try:
    main_element = session1.find_element_by_xpath(Links.PRESS_RELEASES_XPATH.value)
    print('element is displayed')

except TimeoutException:
    print('TimeoutException')
except NoSuchElementException:
    print('NoSuchElementException')


# elements = main_element.find_elements_by_xpath(".//div[@class='categoryBox']")
# elements = list(filter(lambda x: not x.get_attribute('style') == 'display: none;', elements))
# for box in elements:
#     url = box.find_element_by_xpath(".//a").get_attribute('href')
#     link = CbsLink(url)


# for element in elements:
#     style = element.get_attribute('style')
#     # if not style == 'display: none;':
#     a = element.find_element_by_xpath(".//a")
#     print(a.get_attribute('href'))
# CbsPageUtility.set_top_box(page=page1, session=session1)


session1.close()
# print(page1.get_errors())

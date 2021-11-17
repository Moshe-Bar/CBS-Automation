# -*- coding: cp1252 -*-
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from DataBase.DataBase import Links
from Utility.WebPartUtility import WebPartUtility
from Utility.TestUtility import TestUtility












# URL = r"D:\Current\Selenium\NewAutomationEnv\DataBase\local\test_2.html"
URL = r"https://www.cbs.gov.il/he/subjects/Pages/-%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%9C%D7%A4%D7%99-%D7%9E%D7%95%D7%A6%D7%90.aspx"

sess = TestUtility.create_web_driver(wait_time=10)


page = SubjectPage(CbsLink(url=URL), '????? ??')
sess.get(URL)
print('test is started')


elem = sess.find_element(By.XPATH,"//div[@id='hebstats']")
print('stats ready..')
try:
    e = elem.find_element(By.XPATH,"./div[@class='ms-webpart-chrome ms-webpart-chrome-fullWidth ']")
    print('is displayed: ',elem.is_displayed())
    print('hidden')
except NoSuchElementException:
    print('hidden state div not found')


# WebPartUtility.set_international_comparisons(page=page, session=sess)
# print(page.error_to_str())


# try:
#     # e = sess.find_element_by_xpath("//div[@class='generalBox'][3]//h2//span").text
#     # text_e = e.find_element_by_xpath(".//h2//span").text
#
#     b = sess.find_element_by_xpath(Links.INTERNATIONAL_COMPARISONS_XPATH.value)
#     sess.execute_script("arguments[0].style.display = 'block';", b)
#     text = b.find_element_by_xpath(".//h2//span").text
#     # text_b = b.find_element_by_xpath(".//h2//span").text
#     # print("element links: ",e)
#     print("element conferences: ",text)
# except Exception as e:
#     print("exception was raised: ",e)
#     pass
# CbsPageUtility.set_sub_subjects(page=page, session=sess)
# WebPartUtility.set_geographic_zone(page=page,session =sess)

# WebPartUtility.set_heb_statistical(page=page, root_element=sess)
# WebPartUtility.set_extra_parts(page=page, root_element=sess)
# WebPartUtility.set_press_releases(page=page, session=sess)
# CbsPageUtility.set_sub_subjects(page=page, session=sess)
# print('errors:' ,page.error_to_str())
print('end of test')
sess.close()

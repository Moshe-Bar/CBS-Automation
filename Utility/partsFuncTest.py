# -*- coding: cp1252 -*-
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from DataBase.DataBase import Links
from Utility.WebPartUtility import WebPartUtility, ROOT_ELEMENT, XPATH
from Utility.TestUtility import TestUtility
from selenium.webdriver.support import expected_conditions as EC












# URL = r"D:\Current\Selenium\NewAutomationEnv\DataBase\local\test_2.html"
URL = r"https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94.aspx"

sess = TestUtility.create_web_driver(wait_time=10)


page = SubjectPage(CbsLink(url=URL), 'population')
sess.get(URL)

print('test is started')

xpath = ROOT_ELEMENT + XPATH['HEBREW_STATS_XPATH']

try:
    # e = sess.find_element(By.XPATH,Links.ROOT_XPATH.value+Links.HEBREW_STATS_XPATH.value)
    # WebPartUtility.set_heb_statistical(page=page, session=sess)
    # WebPartUtility.set_extra_parts(page=page,root_element=sess)
    # WebPartUtility.set_summary(page=page, session=sess)
    # WebPartUtility.set_international_comparisons(page=page, session=sess)
    # WebPartUtility.set_more_links(page=page, session=sess)
    try:
        element = WebDriverWait(sess, 10).until(
            EC.presence_of_element_located((By.XPATH, ROOT_ELEMENT))
        )
        WebPartUtility.set_heb_statistical(page=page, session=element)
        WebPartUtility.set_extra_parts(page=page,root_element=element)
        WebPartUtility.set_summary(page=page, session=element)
        WebPartUtility.set_international_comparisons(page=page, session=element)
        WebPartUtility.set_more_links(page=page, session=element)
        WebPartUtility.set_geographic_zone(page=page, session=element)
        WebPartUtility.set_publications(page=page, session=element)
        WebPartUtility.set_tools_and_db(page=page, session=element)
        WebPartUtility.set_press_releases(page=page, session=element)
        WebPartUtility.set_sub_subjects(page=page, session=element)
        WebPartUtility.set_top_box(page=page, session=element)
        WebPartUtility.set_tables_and_charts(page=page, session=element)

        # print(element)
    except NoSuchElementException:
        print("couldn't find main html")
    finally:
        sess.quit()
    # print("path: {}".format(xpath))
    # e = sess.find_element(By.XPATH, xpath)
    # root_element, error = WebPartUtility.get_main_element('HEBREW_STATS_XPATH', sess)
    # print(error)
    # WebPartUtility.set_geographic_zone(page=page, session=sess)
    # WebPartUtility.set_publications(page=page, session=sess)
    # WebPartUtility.set_tools_and_db(page=page, session=sess)
    # WebPartUtility.set_press_releases(page=page, session=sess)
    # WebPartUtility.set_sub_subjects(page=page, session=sess)
    # WebPartUtility.set_top_box(page=page, session=sess)
    # WebPartUtility.set_tables_and_charts(page=page, session=sess)

    # print('test functions ended')
    # print('errors: ',page.error_to_str())
except NoSuchElementException:
    print("couldn't find main html")


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
# sess.close()

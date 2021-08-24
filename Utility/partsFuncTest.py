# -*- coding: cp1252 -*-
from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from Utility.WebPartUtility import WebPartUtility
from Utility.TestUtility import TestUtility

# URL = r"D:\Current\Selenium\NewAutomationEnv\DataBase\local\test_2.html"
URL = r"https://www.cbs.gov.il/he/subjects/Pages/%D7%AA%D7%97%D7%96%D7%99%D7%95%D7%AA-%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94.aspx"

sess = TestUtility.create_web_driver(wait_time=10)


page = SubjectPage(CbsLink(url=URL), '????? ??')
sess.get(URL)
print('test is started')
# CbsPageUtility.set_sub_subjects(page=page, session=sess)
WebPartUtility.set_heb_statistical(page=page, root_element=sess)
WebPartUtility.set_extra_parts(page=page, root_element=sess)
# WebPartUtility.set_press_releases(page=page, session=sess)
# CbsPageUtility.set_sub_subjects(page=page, session=sess)
print(page.error_to_str())
print('end of test')
sess.close()

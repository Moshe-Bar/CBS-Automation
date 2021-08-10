# -*- coding: cp1252 -*-
from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from Testing.CbsPageUtility import CbsPageUtility
from Testing.TestUtility import TestUtility

URL = r'D:\Current\Selenium\NewAutomationEnv\dataBase\htmlPages\test_page.html'

sess = TestUtility.create_web_driver(wait_time=10)

page = SubjectPage(CbsLink(url=URL), '????? ??')
sess.get(URL)
print('test is started')
# CbsPageUtility.set_sub_subjects(page=page, session=sess)
CbsPageUtility.set_press_releases(page=page, session=sess)
# CbsPageUtility.set_sub_subjects(page=page, session=sess)
print(page.press_releases.errors)
print('end of test')
sess.close()

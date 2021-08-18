# -*- coding: cp1252 -*-
from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from Utility.CbsPageUtility import CbsPageUtility
from Utility.TestUtility import TestUtility

# URL = r"D:\Current\Selenium\NewAutomationEnv\dataBase\htmlPages\test_2.html"
URL = r"https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94.aspx"

sess = TestUtility.create_web_driver(wait_time=10)


page = SubjectPage(CbsLink(url=URL), '????? ??')
sess.get(URL)
print('test is started')
# CbsPageUtility.set_sub_subjects(page=page, session=sess)
CbsPageUtility.set_tables_and_charts(page=page, session=sess)
# CbsPageUtility.set_sub_subjects(page=page, session=sess)
print(page.tables_and_charts.errors)
print('end of test')
sess.close()

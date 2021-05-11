# -*- coding: cp1252 -*-
from CbsClasses.CbsLink import CbsLink
from CbsClasses.CbsPage import CbsPage
from Testing.CbsPageUtility import CbsPageUtility
from Testing.TestUtility import TestUtility

URL = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%9C%D7%99%D7%93%D7%95%D7%AA-%D7%97%D7%99.aspx'

sess = TestUtility.create_web_driver(wait_time=10)

page = CbsPage(CbsLink(url=URL), '????? ??')
sess.get(URL)
print('test is started')
# CbsPageUtility.set_sub_subjects(page=page, session=sess)
CbsPageUtility.set_more_links(page=page, session=sess)
# CbsPageUtility.set_sub_subjects(page=page, session=sess)
# print(page.sub_subjects.errors)
print(page.more_links.errors)
print('end of test')
sess.close()

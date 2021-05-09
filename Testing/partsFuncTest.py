# -*- coding: cp1252 -*-
from CbsClasses.CbsLink import CbsLink
from CbsClasses.CbsPage import CbsPage
from Testing.CbsPageUtility import CbsPageUtility
from Testing.TestUtility import TestUtility

URL = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA.aspx'

sess = TestUtility.create_web_driver(10)
page = CbsPage(CbsLink(url=URL), '??????')
sess.get(URL)
print('test is start')
CbsPageUtility.set_sub_subjects(page=page, session=sess)
# print(page.sub_subjects.errors)
sess.close()

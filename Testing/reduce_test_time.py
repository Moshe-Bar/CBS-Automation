import threading
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from Testing.CbsPageUtility import CbsPageUtility
from Testing.TestUtility import TestUtility

URL1 = r'https://www.cbs.gov.il/he/subjects/Pages/%D7%A2%D7%95%D7%91%D7%93%D7%99%D7%9D-%D7%9E%D7%97%D7%95%D7%9C.aspx'

# lu = CbsLink('https://www.cbs.gov.il/he/PublishingImages/statistical/stat164.JPG')
# CbsPageUtility.set_link_status(lu)
# print(lu.status_code)

page1 = SubjectPage(CbsLink(URL1),'עובדים מחול')
session1 = TestUtility.create_web_driver()
session1.get(page1.link.url)

CbsPageUtility.set_heb_statistical(page=page1, root_element=session1)
# CbsPageUtility.set_press_releases(page=page1, root_element=session1)
session1.close()
print(page1.get_errors())




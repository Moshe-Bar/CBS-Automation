
from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from Testing.CbsPageUtility import CbsPageUtility
from Testing.TestUtility import TestUtility

# URL1 = r'https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%9C%D7%A4%D7%99-%D7%A6%D7%95%D7%A8%D7%AA-%D7%99%D7%99%D7%A9%D7%95%D7%91.aspx'
URL1 = r'D:\Current\Selenium\NewAutomationEnv\dataBase\htmlPages\נושאים - אוכלוסייה לפי צורת יישוב.html'

# lu = CbsLink('https://www.cbs.gov.il/he/PublishingImages/statistical/stat164.JPG')
# CbsPageUtility.set_link_status(lu)
# print(lu.status_code)

page1 = SubjectPage(CbsLink(URL1) ,'אוכלוסייה לפי צורת יישוב')
session1 = TestUtility.create_web_driver()
session1.get(page1.link.url)

# CbsPageUtility.set_heb_statistical(page=page1, root_element=session1)
# CbsPageUtility.set_sub_subjects(page=page1, root_element=session1)
# CbsPageUtility.set_extra_parts(page=page1, root_element=session1)
CbsPageUtility.set_tools_and_db(page=page1, root_element=session1)


# CbsPageUtility.set_press_releases(page=page1, root_element=session1)
session1.close()
print(page1.get_errors())

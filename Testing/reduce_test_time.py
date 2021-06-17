
from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from Testing.CbsPageUtility import CbsPageUtility
from Testing.TestUtility import TestUtility

URL1 = r'D:\Current\Selenium\NewAutomationEnv\dataBase\htmlPages\נושאים - בריאות.html'



page1 = SubjectPage(CbsLink(URL1) ,'בריאות מקומי')
session1 = TestUtility.create_web_driver()
session1.get(page1.link.url)


CbsPageUtility.set_summary(page=page1, session=session1)


session1.close()
print(page1.get_errors())

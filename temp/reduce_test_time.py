import requests

from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage

from Utility.TestUtility import TestUtility

URL1 = r"D:\Current\Selenium\NewAutomationEnv\DataBase\local\נושאים - אוכלוסייה.mhtml"

page1 = SubjectPage(CbsLink(URL1), 'בריאות מקומי')
session1 = TestUtility.create_web_driver()
session1.get(page1.link.url)

r = requests.get(
    'https://www.cbs.gov.il/he/Pages/%D7%9B%D7%9C-%D7%94%D7%9E%D7%95%D7%A0%D7%97%D7%99%D7%9D.aspx?TID=%D7%99%D7%9C%D7%95%D7%93%D7%94%20%D7%95%D7%A4%D7%A8%D7%99%D7%95%D7%9F&TID1=%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA&TID2=%D7%99%D7%9C%D7%95%D7%93%D7%94%20%D7%95%D7%A4%D7%A8%D7%99%D7%95%D7%9F')
print(r.status_code)

session1.close()
# print(page1.get_errors())

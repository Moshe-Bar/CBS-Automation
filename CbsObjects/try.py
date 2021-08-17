from selenium import webdriver

from Utility.CbsPageUtility import CbsPageUtility
from CbsObjects.Pages.SubjectPage import SubjectPage

kaspersky = 'C:\ProgramData\Kaspersky Lab\AVP21.3\QB'

url = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%9C%D7%99%D7%93%D7%95%D7%AA-%D7%97%D7%99.aspx'
CBS_HOME_PAGE = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94.aspx'
ERROR_PAGE = 'https://www.cbs.gov.il/he/About/Documents/mediniyut-pirsum.pdf'
WEB_PARTS_ERROR = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%A8%D7%95%D7%95%D7%97%D7%AA-%D7%94%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%95%D7%A2%D7%9E%D7%93%D7%95%D7%AA-%D7%9B%D7%9C%D7%A4%D7%99-%D7%A9%D7%99%D7%A8%D7%95%D7%AA%D7%99-%D7%9E%D7%9E%D7%A9%D7%9C-2007.aspx '
test_page = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%A8%D7%95%D7%95%D7%97%D7%AA-%D7%94%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%95%D7%A2%D7%9E%D7%93%D7%95%D7%AA-%D7%9B%D7%9C%D7%A4%D7%99-%D7%A9%D7%99%D7%A8%D7%95%D7%AA%D7%99-%D7%9E%D7%9E%D7%A9%D7%9C-2007.aspx'


def test(page: SubjectPage, session: webdriver.Chrome):
    elem = session.find_element_by_xpath("//div[@id='hebstats']//div[@style='display: none;']")
    print(elem)


# driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
# driver.implicitly_wait(10)  # seconds
# driver.get(page)
# page = CbsPage(CbsLink(r'https://www.cbs.gov.il/he/subjects/Pages/%D7%A8%D7%95%D7%95%D7%97%D7%94.aspx'), 'test')
# page.link.status_code = 200
# driver.get(r'https://www.cbs.gov.il/he/subjects/Pages/%D7%A8%D7%95%D7%95%D7%97%D7%94.aspx')
# set_MomentOfStatistics_part(page, driver)
# print(page.stats_part.errors)
# print(page.stats_part.isHidden)
for page in CbsPageUtility.get_cbs_map_pages():
    print(page.link.url)
# test(page, driver)
# driver.close()

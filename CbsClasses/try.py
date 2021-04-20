from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from CbsPageUtility import CbsPageUtility
from CbsClasses.CbsLink import CbsLink
from CbsClasses.CbsPage import CbsPage
from LinksUtility.usefulLinks import Links

kaspersky = 'C:\ProgramData\Kaspersky Lab\AVP21.3\QB'

url = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%9C%D7%99%D7%93%D7%95%D7%AA-%D7%97%D7%99.aspx'
CBS_HOME_PAGE = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94.aspx'
ERROR_PAGE = 'https://www.cbs.gov.il/he/About/Documents/mediniyut-pirsum.pdf'
WEB_PARTS_ERROR = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%A8%D7%95%D7%95%D7%97%D7%AA-%D7%94%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%95%D7%A2%D7%9E%D7%93%D7%95%D7%AA-%D7%9B%D7%9C%D7%A4%D7%99-%D7%A9%D7%99%D7%A8%D7%95%D7%AA%D7%99-%D7%9E%D7%9E%D7%A9%D7%9C-2007.aspx '
test_page = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%A8%D7%95%D7%95%D7%97%D7%AA-%D7%94%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%95%D7%A2%D7%9E%D7%93%D7%95%D7%AA-%D7%9B%D7%9C%D7%A4%D7%99-%D7%A9%D7%99%D7%A8%D7%95%D7%AA%D7%99-%D7%9E%D7%9E%D7%A9%D7%9C-2007.aspx'


# only for hebrew page
def set_MomentOfStatistics_part(session: webdriver.Chrome, page: CbsPage):
    driver.implicitly_wait(10)
    # *****************************************************************************************************************
    # check for extra web part - empty statistical (different xPath)
    try:
        session.find_element_by_xpath("//div[@id='MSOZoneCell_WebPartWPQ13']")
        page.stats_part.errors.append('error: statistical - extra web part')
    except  NoSuchElementException:
        # empty extra web part is not exist 200
        pass
    # *****************************************************************************************************************
    try:
        # in case stats is hidden there is nothing to check
        session.find_elements_by_xpath("//div[@id='hebstats']//div[@style='display:none']")
        page.stats_part.isHidden = True
        return
    except NoSuchElementException:
        #   in case the web part is showed need to  be check (it displayed)
        page.stats_part.isHidden = False
        s_pages_images = session.find_elements_by_xpath("//div[@id='hebstats']//ul[@class='cbs-List']//li//img")
        s_pages_links = session.find_elements_by_xpath("//div[@id='hebstats']//ul[@class='cbs-List']//li//a")
        if len(s_pages_images) == 0:
            page.stats_part.errors.append('images content is missing in Statistical')
        else:
            for i, img in enumerate(s_pages_images):
                cur_link = CbsLink(img.get_attribute('src'))
                CbsPageUtility.set_link_status(cur_link)
                page.stats_part.images.append(cur_link)
                if not cur_link.status_code == 200:
                    page.stats_part.errors.append('image is broken in Statistical')
        if len(s_pages_links) == 0:
            page.stats_part.errors.append('links content is missing in Statistical')
        else:
            for i, sheet in enumerate(s_pages_links):
                cur_link = CbsLink(sheet.get_attribute('href'))
                page.stats_part.images.append(cur_link)
                CbsPageUtility.set_link_status(cur_link)
                if not cur_link.status_code == 200:
                    page.stats_part.errors.append('link is broken in Statistical')
    # *****************************************************************************************************************
    try:
        all_stats_link = session.find_element_by_xpath(
            "//div[@id='hebstats']//a[contains(text(),'לכל עלוני הסטטיסטיקל')]")
        cur_link = CbsLink(all_stats_link.get_attribute('href'))
        page.stats_part.links.append(cur_link)
        CbsPageUtility.set_link_status(cur_link)
        if not cur_link.status_code == 200:
            page.stats_part.errors.append('link to all massages is broken in Statistical')
    except NoSuchElementException:
        page.stats_part.errors.append('link to all massages is missing in Statistical')
    # *****************************************************************************************************************


driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
driver.implicitly_wait(10)  # seconds
# driver.get(page)
page = CbsPage(CbsLink('https://www.cbs.gov.il/he/Statistics/Pages/%D7%9B%D7%9C%D7%99%D7%9D-%D7%95%D7%9E%D7%90%D7%92%D7%A8%D7%99-%D7%A0%D7%AA%D7%95%D7%A0%D7%99%D7%9D.aspx'), 'רווחת-האוכלוסייה-ועמדות-כלפי-שירותי-ממשל-2007')
page.link.status_code = 200
driver.get('https://www.cbs.gov.il/he/Statistics/Pages/%D7%9B%D7%9C%D7%99%D7%9D-%D7%95%D7%9E%D7%90%D7%92%D7%A8%D7%99-%D7%A0%D7%AA%D7%95%D7%A0%D7%99%D7%9D.aspx')
set_MomentOfStatistics_part(driver, page)
print(page.stats_part.errors)
driver.close()

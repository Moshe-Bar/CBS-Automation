from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from CbsClasses.CbsLink import CbsLink
from CbsClasses.CbsPageUtility import CbsPageUtility
from LinksUtility.usefulLinks import Links

driver = CbsPageUtility.create_web_driver(20)
driver.get('https://www.cbs.gov.il/he/subjects/Pages/%D7%91%D7%A8%D7%99%D7%90%D7%95%D7%AA.aspx')

s = driver.find_elements_by_xpath("//div[@class='twoColumn']//a[@href]")

print('num of showed elements: ' + str(len(s)))
links = []
not_links = []
for link in s:
    cbs_link = CbsLink(link.get_attribute('href'))
    cbs_link.name = link.text
    if cbs_link.link =='':
        if not cbs_link.name == '':
            not_links.append(cbs_link)
    if cbs_link.link.startswith('http'):

    if cbs_link.link.startswith('javascript'):
for link in links:
    print(link.name + '::' + link.link)
print('num after filter: ' + str(len(links)))
for link in not_links:
    print(link.name + '::' + link.link)

driver.close()

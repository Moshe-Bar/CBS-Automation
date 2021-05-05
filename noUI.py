from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DRIVER_PATH = 'C:\chromedriver.exe'

# options = Options()
# options.headless = True
options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(DRIVER_PATH, options=options)


driver.get(r'https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94.aspx')
print(driver.find_element_by_xpath("//div[@class='edit-mode-panel title-edit']").text[::-1])
driver.close()


# driver.get(r'https://www.cbs.gov.il/he/subjects/Pages/%D7%A7%D7%A9%D7%99%D7%A9%D7%99%D7%9D.aspx')

from selenium import webdriver

from dataBase.DataBase import Links
from UI.MainProcess_old import getCurrentLinks
#
driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
driver.implicitly_wait(20)
driver.get(Links.CBS_MAP_SITE_HE.value)
raw_list = getCurrentLinks(driver)
link_list = list(
        map(lambda x: (x.get_attribute('href'), x.text), raw_list))
with open('heb_pages_links.txt', 'w') as f:
    for link in link_list:
        f.write(link[0] + ' ' + link[1] + '\n')
    f.close()


links = []
with open('heb_pages_links.txt', 'r') as f:
    for line in f:
        links.append(line)
    f.close()
print(links[1])
driver.close()
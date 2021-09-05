from selenium import webdriver

from DL.DataBase import Links
from temp.MainProcess_old import getCurrentLinks

#
driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
driver.implicitly_wait(20)
driver.get(Links.CBS_MAP_SITE_EN.value)
raw_list = getCurrentLinks(driver)
link_list = list(
    map(lambda x: (x.get_attribute('href'), x.text), raw_list))
with open('en_pages_links.txt', 'w') as f:
    for link in link_list:
        f.write(link[0] + ' ' + link[1] + '\n')
    f.close()

#test--------------------------------------
links = []
with open('en_pages_links.txt', 'r') as f:
    for line in f:
        links.append(line)
    f.close()
print(links[1])
driver.close()

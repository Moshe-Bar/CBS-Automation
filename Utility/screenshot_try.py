from selenium import webdriver
from PIL import Image

# take screenshot
from DL import Links

driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
driver.get('https://www.cbs.gov.il/he/subjects/Pages/%D7%A8%D7%95%D7%95%D7%97%D7%94.aspx')
driver.maximize_window()
element = driver.find_element_by_xpath(Links.HEBREW_STATS_XPATH.value)
location = element.location
# print(element.size)
# print(element.location)
size = element.size
driver.save_screenshot("pageImage.png")

# crop image
x = location['x']
y = location['y']
width = location['x']+size['width']
height = location['y']+size['height']
im = Image.open('../temp/pageImage.png')
im = im.crop((int(x), int(y), int(width), int(height)))
im.save('element.png')

driver.quit()
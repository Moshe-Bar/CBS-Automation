import time

import grequests
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def getCurrentLinks(driver):
    # finding the LinksUtility in the page
    print('finding all HREF objects...')
    uList = driver.find_elements_by_xpath(
        "//ul[@class='level1 sitemapmenu']//li[@class='ng-scope']//ul[@class='level2']//li[@class='ng-scope']//ul["
        "@class='level3']//li//a")
    return uList


# Then we create a bunch of workers.
# prepare the sessions
# payload = {'apikey': 1, 'locale': enGB}
from selenium import webdriver

from DL.DataBase import Links

start_time = time.time()
NUM_SESSIONS = 20
sessions = [requests.Session() for i in range(NUM_SESSIONS)]
# rules for retry
retries = Retry(total=3,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504])
# implements the rules in sessions
for s in sessions:
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))

# After that, we can create all the requests we need to perform, and spread them out between the workers using modulo.
driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
driver.implicitly_wait(10)
driver.get(Links.CBS_MAP_SITE_HE.value)
raw_list = getCurrentLinks(driver)
l_list = list(
    map(lambda x: x.get_attribute('href'), raw_list))

# ************************************************************8
urls = l_list  # Insert massive list of URLs here.

reqs = []
i = 0

for url in urls:
    reqs.append(grequests.get(url, session=sessions[i % NUM_SESSIONS]))
    i += 1
print(reqs)
# Now, we can call grequests.map() to execute all of our calls asynchronously.
responses = grequests.map(reqs, size=NUM_SESSIONS)

# The responses object will now be a list of Response objects. You can iterate over this list to access the results.
# for r in responses:
#     print(r.status_code)  # Access the status_code code we got back from the server. 200, 404 etc.
#     # print(r.json())  # We can decode JSON straight into a dictionary for easy processing, just like usual.
print(str(time.time() - start_time) + 'for this code')
driver.close()

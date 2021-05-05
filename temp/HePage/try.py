# from selenium import webdriver

# from seleniumwire import webdriver  # Import from seleniumwire
from DataBase import Links

ERRORS = ['Sorry, the page is not found', 'מתנצלים, הדף לא נמצא']
URL = 'https://www.cbs.gov.il/he/About/Documents/idkun_h.pdf'


# URL = 'https://www.cbs.gov.il/he/Pages/45454'


# s = driver.find_elements_by_xpath("//div[@class='twoColumn']//a[@href]")
#
# print('num of showed elements: ' + str(len(s)))
# links = []
# not_links = []
# for link in s:
#     cbs_link = CbsLink(link.get_attribute('href'))
#     cbs_link.name = link.text
#     if cbs_link.url == '':
#         if not cbs_link.name == '':
#             not_links.append(cbs_link)
#     if cbs_link.url.startswith('http'):
#         if cbs_link.url.startswith('javascript'):
#             for link in links:
#                 print(link.name + '::' + link.link)
#             print('num after filter: ' + str(len(links)))
#             for link in not_links:
#                 print(link.name + '::' + link.url)

def func():
    # content = session.page_source
    # for text in ERRORS:
    #     if text in content:
    #         print(True)
    #     else:
    #         print(False)
    #
    # session.get(
    #     'https://www.cbs.gov.il/he/subjects/Pages/%D7%A8%D7%95%D7%95%D7%97%D7%AA-%D7%94%D7%90%D7%95%D7%9B%D7%9C%D7%95'
    #     '%D7%A1%D7%99%D7%99%D7%94-%D7%95%D7%A2%D7%9E%D7%93%D7%95%D7%AA-%D7%9B%D7%9C%D7%A4%D7%99-%D7%A9%D7%99%D7%A8%D7'
    #     '%95%D7%AA%D7%99-%D7%9E%D7%9E%D7%A9%D7%9C-2007.aspx')
    # content = session.page_source
    # for text in ERRORS:
    #     if text in content:
    #         print(True)
    #     else:
    #         print(False)

    # Create a new instance of the Firefox driver
    driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
    driver.implicitly_wait(20)

    # Go to the Google home page
    driver.get('https://www.cbs.gov.il/he/Pages/45454')
    print(driver.requests)

    # Access and print requests via the `requests` attribute
    for request in driver.requests:
        if request.response:
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type'])


# driver = CbsPageUtility.create_web_driver(20)
# driver.get(URL)
func()
# driver.close()

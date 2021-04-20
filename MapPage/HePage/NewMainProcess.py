import time
from selenium import webdriver
from CbsClasses import CbsPageUtility
from CbsClasses.CbsPage import CbsPage
from LinksUtility.usefulLinks import Links


def getCurrentLinks(driver):
    # finding the LinksUtility in the page
    print('finding all HREF objects...')
    uList = driver.find_elements_by_xpath(
        "//ul[@class='level1 sitemapmenu']//li[@class='ng-scope']//ul[@class='level2']//li[@class='ng-scope']//ul["
        "@class='level3']//li//a")
    return uList


def test_pages_links(pages: [CbsPage]):
    for page in pages:
        CbsPageUtility.CbsPageUtility.checkLink(page.get_link())
        print(str(page))


def main():
    start_time = time.time()
    # initial selenium driver
    driver = CbsPageUtility.CbsPageUtility.create_web_driver(20)
    driver.get(Links.CBS_MAP_SITE_HE.value)
    raw_list = getCurrentLinks(driver)

    # arranging the LinksUtility in an appropriate list
    print('number of cbs_link objects found : ', len(raw_list))
    # for english site '[::-1]' need to be deleteted
    link_list = list(
        map(lambda x: (x.get_attribute('href'), x.text), raw_list))
    # generate pages
    pages = CbsPageUtility.CbsPageUtility.create_pages(link_list)
    # checking the Links chronically
    test_pages_links(pages)

    # check for page links corrupted
    pages_broken_links = []
    print('broken links: ')
    for page in pages_broken_links:
        print(str(page))

    driver.close()
    print(str(time.time() - start_time))


if __name__ == "__main__":
    main()

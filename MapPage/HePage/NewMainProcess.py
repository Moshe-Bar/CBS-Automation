import time
from selenium import webdriver
from CbsClasses.CbsPageUtility import CbsPageUtility
from CbsClasses.CbsLink import CbsLink
from CbsClasses.CbsPage import CbsPage
from LinksUtility.usefulLinks import Links


def getCurrentLinks(driver):
    driver.get(Links.CBS_MAP_SITE_HE.value)
    # finding the LinksUtility in the page
    print('finding all HREF objects...')
    uList = driver.find_elements_by_xpath(
        "//ul[@class='level1 sitemapmenu']//li[@class='ng-scope']//ul[@class='level2']//li[@class='ng-scope']//ul["
        "@class='level3']//li//a")
    return uList


def test_pages_links(pages: [CbsPage]):
    for page in pages:
        CbsPageUtility.set_link_status(page.get_link())
        print(str(page))
        for link in page:
            CbsPageUtility.set_link_status(link)


def main():
    start_time = time.time()
    # initial selenium driver
    driver = CbsPageUtility.create_web_driver(20)
    raw_list = getCurrentLinks(driver)

    # arranging the LinksUtility in an appropriate list
    print('number of cbs_link objects found : ', len(raw_list))
    # for english site '[::-1]' need to be deleted

    link_list = list(
        map(lambda x: CbsLink(x.get_attribute('href')), raw_list))

    for index, link in enumerate(raw_list):
        link_list[index].name = link.text
    # generate pages
    pages = CbsPageUtility.create_pages(link_list)
    # checking the Links chronically
    # test_pages_links(pages)
    print('before')
    for page in pages:
        # CbsPageUtility.set_internal_links(page, driver)
        driver.get(page.link.url)
        CbsPageUtility.set_MomentOfStatistics_part(page, driver)
        if len(page.stats_part.errors) > 0:
            print(page.name)
            print(page.stats_part.errors)

        # driver.implicitly_wait(10)

    driver.close()
    # for page in pages:
    #     if len(page.stats_part.errors)!=0:
    #         print(page.link.url + '::' + page.stats_part.errors)
    print(str(time.time() - start_time))


if __name__ == "__main__":
    main()

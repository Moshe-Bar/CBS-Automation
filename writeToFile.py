import json

from selenium import webdriver

from LinksUtility.usefulLinks import Links


def wrightToFile(list_of_links):
    with open('links.json', 'w') as file:
        data = {'links': list_of_links}
        print(data)
        json.dump(data, file)
        file.close()


def readFile():
    with open('links.json') as f:
        data = json.load(f)
        f.close()
        return data['links']


def getCurrentLinks(driver):
    # finding the LinksUtility in the page
    print('finding all HREF objects...')
    uList = driver.find_elements_by_xpath(
        "//ul[@class='level1 sitemapmenu']//cbs_link[@class='ng-scope']//ul[@class='level2']//cbs_link[@class='ng-scope']//ul["
        "@class='level3']//cbs_link//a")
    return uList


def main():
    # initial selenium driver
    driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
    driver.get(Links.CBS_MAP_SITE_HE.value)
    raw_list = getCurrentLinks(driver)

    # arranging the LinksUtility in an appropriate list
    print('number of cbs_link objects found : ', len(raw_list))
    # for english site '[::-1]' need to be deleteted
    link_list = list(
        map(lambda x: x.get_attribute('href'), raw_list))

    wrightToFile(link_list)

    driver.close()


if __name__ == '__main__':
    main()

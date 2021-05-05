import unittest
from selenium import webdriver
from Testing import CbsPageUtility
from DataBase import Links


class MyTestCase(unittest.TestCase):
    def test_PageLevel(self):
        driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
        driver.get(
            'https://www.cbs.gov.il/he/subjects/Pages/%D7%94%D7%9B%D7%A0%D7%A1%D7%95%D7%AA-%D7%95%D7%94%D7%95%D7%A6'
            '%D7%90%D7%95%D7%AA-%D7%9E%D7%A9%D7%A7-%D7%91%D7%99%D7%AA.aspx')
        self.assertEqual(CbsPageUtility.CbsPageUtility.findPageLevel(driver), 2)
        driver.get(
            'https://www.cbs.gov.il/he/subjects/Pages/%D7%A9%D7%95%D7%A7-%D7%94%D7%A2%D7%91%D7%95%D7%93%D7%94.aspx')
        self.assertEqual(CbsPageUtility.CbsPageUtility.findPageLevel(driver), 1)
        driver.get(
            'https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%9C%D7%A4%D7%99-%D7%93%D7%AA-%D7%95%D7%A7%D7%91%D7%95%D7%A6%D7%AA-%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94.aspx')
        self.assertEqual(CbsPageUtility.CbsPageUtility.findPageLevel(driver), 3)
        driver.close()

    def test_PageParent(self):
        driver = webdriver.Chrome(Links.CHROME_DRIVER.value)
        driver.get('https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94'
                   '-%D7%9C%D7%A4%D7%99-%D7%93%D7%AA-%D7%95%D7%A7%D7%91%D7%95%D7%A6%D7%AA-%D7%90%D7%95%D7%9B%D7%9C%D7'
                   '%95%D7%A1%D7%99%D7%99%D7%94.aspx')
        self.assertEqual('https://www.cbs.gov.il/he/subjects/Pages/%D7%AA%D7%9B%D7%95%D7%A0%D7%95%D7%AA-%D7%93%D7%9E'
                         '%D7%95%D7%92%D7%A8%D7%A4%D7%99%D7%95%D7%AA.aspx',
                         CbsPageUtility.CbsPageUtility.findPageParent(driver))

if __name__ == '__main__':
    unittest.main()

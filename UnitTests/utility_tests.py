import unittest
from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage

from Utility.TestUtility import TestUtility
from Utility.WebPartUtility import WebPartUtility


class MyTestCase(unittest.TestCase):
    def __init__(self):
        super().__init__()


        URL = r"D:\Current\Selenium\NewAutomationEnv\DataBase\local\test_2.html"
        # URL = r"https://www.cbs.gov.il/he/subjects/Pages/%D7%94%D7%95%D7%A6%D7%90%D7%94-%D7%9C%D7%90%D7%95%D7%9E%D7%99%D7%AA-%D7%9C%D7%AA%D7%A8%D7%91%D7%95%D7%AA-%D7%9C%D7%91%D7%99%D7%93%D7%95%D7%A8-%D7%95%D7%9C%D7%A1%D7%A4%D7%95%D7%A8%D7%98.aspx"

        sess = TestUtility.create_web_driver(wait_time=10)

        page = SubjectPage(CbsLink(url=URL), '????? ??')
        sess.get(URL)
        print('test is started')
        # CbsPageUtility.set_sub_subjects(page=page, session=sess)
        WebPartUtility.set_tables_and_charts(page=page, session=sess)
        # CbsPageUtility.set_sub_subjects(page=page, session=sess)
        print(page.tables_and_charts.errors)
        print('end of test')
        sess.close()


    def test_heb_statistical(self):
        WebPartUtility.set_heb_statistical(page=page, root_element=main_element)
        self.assertEqual(True, False)  # add assertion here

    def test_extra_parts(self):
        WebPartUtility.set_extra_parts(page=page, root_element=main_element)
        self.assertEqual(True, False)  # add assertion here

    def test_summary(self):
        WebPartUtility.set_summary(page=page, session=main_element)
        self.assertEqual(True, False)  # add assertion here

    def test_top_box(self):
        WebPartUtility.set_top_box(page=page, session=main_element)
        self.assertEqual(True, False)  # add assertion here

    def test_sub_subjects(self):
        WebPartUtility.set_sub_subjects(page=page, session=main_element)
        self.assertEqual(True, False)  # add assertion here

    def test_press_releases(self):
        WebPartUtility.set_press_releases(page=page, session=main_element)
        self.assertEqual(True, False)  # add assertion here

    def test_ables_and_charts(self):
        WebPartUtility.set_tables_and_charts(page=page, session=main_element)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

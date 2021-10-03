import unittest
from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage

from Utility.TestUtility import TestUtility
from Utility.WebPartUtility import WebPartUtility

SESSION = TestUtility.create_web_driver(wait_time=10)


class MyTestCase(unittest.TestCase):

    def test_heb_statistical(self):
        print('statistical test...')
        # page with errors
        url_0 = 'https://www.cbs.gov.il/he/subjects/Pages/-%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%9C%D7%A4%D7%99-%D7%9E%D7%95%D7%A6%D7%90.aspx'
        # page without errors
        url_1 = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%AA%D7%9B%D7%95%D7%A0%D7%95%D7%AA-%D7%93%D7%9E%D7%95%D7%92%D7%A8%D7%A4%D7%99%D7%95%D7%AA.aspx'

        page = SubjectPage(CbsLink(url=url_0), '????? ??')
        SESSION.get(url_0)
        WebPartUtility.set_heb_statistical(page=page, root_element=SESSION)
        print('Error page: ', page.error_to_str())
        self.assertEqual(False, len(page.stats_part.get_errors()) == 0)

        page = SubjectPage(CbsLink(url=url_1), '????? ??')
        SESSION.get(url_1)
        WebPartUtility.set_heb_statistical(page=page, root_element=SESSION)
        print('Correct page: ', page.error_to_str())
        self.assertEqual(True, len(page.stats_part.get_errors()) == 0)  # add assertion here

    def test_extra_parts(self):
        url_0 = ''
        url_1 = ''
        page = SubjectPage(CbsLink(url=url_1), '????? ??')
        SESSION.get(url_1)
        WebPartUtility.set_extra_parts(page=page, root_element=SESSION)
        self.assertEqual(True, False)  # add assertion here

    def test_summary(self):
        url_0 = ''
        url_1 = ''
        page = SubjectPage(CbsLink(url=url_1), '????? ??')
        SESSION.get(url_1)
        WebPartUtility.set_summary(page=page, session=SESSION)
        self.assertEqual(True, False)  # add assertion here

    def test_top_box(self):
        url_0 = ''
        url_1 = ''
        page = SubjectPage(CbsLink(url=url_1), '????? ??')
        SESSION.get(url_1)
        WebPartUtility.set_top_box(page=page, session=SESSION)
        self.assertEqual(True, False)  # add assertion here

    def test_sub_subjects(self):
        url_0 = ''
        url_1 = ''
        page = SubjectPage(CbsLink(url=url_1), '????? ??')
        SESSION.get(url_1)
        WebPartUtility.set_sub_subjects(page=page, session=SESSION)
        self.assertEqual(True, False)  # add assertion here

    def test_press_releases(self):
        url_0 = ''
        url_1 = ''
        page = SubjectPage(CbsLink(url=url_1), '????? ??')
        SESSION.get(url_1)
        WebPartUtility.set_press_releases(page=page, session=SESSION)
        self.assertEqual(True, False)  # add assertion here

    def test_tables_and_charts(self):
        url_0 = ''
        url_1 = ''
        page = SubjectPage(CbsLink(url=url_1), '????? ??')
        SESSION.get(url_1)
        WebPartUtility.set_tables_and_charts(page=page, session=SESSION)
        self.assertEqual(True, False)  # add assertion here

    def test_publications(self):
        error_page_url = r'D:\Current\Selenium\NewAutomationEnv\DataBase\local\נושאים - אוכלוסייה תקול.html'
        correct_page_url = r'D:\Current\Selenium\NewAutomationEnv\DataBase\local\נושאים - אוכלוסייה.html'

        page = SubjectPage(CbsLink(url=error_page_url), 'אוכלוסיה תקול')
        SESSION.get(error_page_url)
        WebPartUtility.set_publications(page=page, session=SESSION)
        print('Error page: ', page.error_to_str())
        print('Error page: ', str(page.get_errors()))
        # self.assertEqual(True, len(page.get_errors()) > 0)

        page = SubjectPage(CbsLink(url=correct_page_url), 'אוכלוסיה')
        SESSION.get(correct_page_url)
        WebPartUtility.set_heb_statistical(page=page, root_element=SESSION)
        print('Correct page: ', page.error_to_str())
        print('Correct page: ', str(page.get_errors()))
        # self.assertEqual(True, len(page.stats_part.get_errors()) == 0)  # add assertion here
        # SESSION.close()

if __name__ == '__main__':
    print('unit test is started')
    unittest.main()
    print('unit test ended')
    SESSION.close()

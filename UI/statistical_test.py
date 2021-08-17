# coding=utf8
from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from Utility.CbsPageUtility import CbsPageUtility
from Utility.TestUtility import TestUtility

URL = r'https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%9C%D7%A4%D7%99-%D7%9E%D7%99%D7%9F.aspx'


def main():
    # print('hi')
    page = SubjectPage(CbsLink(url=URL), 'מדד חברתי כלכלי')
    session = TestUtility.create_web_driver(wait_time=10)
    session.get(URL)
    CbsPageUtility.set_heb_statistical(page=page, session=session)
    print(page.stats_part.errors)


if __name__ == "__main__":
    main()

    # pages = TestUtility.get_pages()
    # page = CbsPage(CbsLink(url=URL), 'מדד חברתי כלכלי')
    # session= TestUtility.create_web_driver()
    # CbsPageUtility.set_statistical_part(session=session)

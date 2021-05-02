import time
from selenium import webdriver
from CbsClasses.CbsPageUtility import CbsPageUtility
from CbsClasses.CbsLink import CbsLink
from CbsClasses.CbsPage import CbsPage
from CbsClasses.TestUtility import TestUtility
from LinksUtility.usefulLinks import Links
from multiprocessing import Pool, Queue



def main(shared_data:Queue, progress_status:Queue, end_flag:Queue):
    shared_data.put('initializing test environment...')
    start_time = time.time()
    result = []
    session, pages = TestUtility.initial_test_environment()
    # page1 = CbsPage(CbsLink('https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%9C%D7%A4%D7%99-%D7%9E%D7%A6%D7%91-%D7%9E%D7%A9%D7%A4%D7%97%D7%AA%D7%99.aspx'),'אוכלוסייה לפי מצב משפחתי')
    # page2 = CbsPage(CbsLink('https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%91%D7%99%D7%99%D7%A9%D7%95%D7%91%D7%99%D7%9D.aspx'),'אוכלוסייה ביישובים' )
    # pages = [page1, page2]
    # session = CbsPageUtility.create_web_driver()
    pages_size = len(pages)
    shared_data.put('number of pages: '+ str(pages_size))
    try:
        for i,page in  enumerate(pages):
            # CbsPageUtility.set_internal_links(page, driver)
            if end_flag.qsize() > 0:
                raise Exception('test canceled')
                # outside canceled
            progress_status.put(i/pages_size)
            session.get(page.link.url)
            CbsPageUtility.set_statistical_part(page, session)
            if len(page.stats_part.errors) > 0:
                print(page.name, page.link.url)
                print(page.stats_part.errors)
                shared_data.put(str(page.name)[::-1])
                shared_data.put(page.stats_part.errors)
                result.append((page.name, page.link.url, page.stats_part.errors))
    except Exception as e:
        end_flag.put(e.args)
    finally:
        session.close()
        end_flag.put('end main process')
    print(str(time.time() - start_time))

if __name__ == "__main__":
    main()
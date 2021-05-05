import time
from Testing.CbsPageUtility import CbsPageUtility
from Testing.TestUtility import TestUtility
from multiprocessing import Queue

# test = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%AA%D7%97%D7%9C%D7%95%D7%90%D7%94.aspx'


def main(shared_data:Queue, progress_status:Queue, end_flag:Queue, pages = []):
    shared_data.put('initializing test environment...')
    start_time = time.time()
    result = []
    try:
        session= TestUtility.get_sessions()# default as synchronous test - one instance session
        if not pages:
            pages = TestUtility.get_pages()
        print('session: ', session) # delete
    except Exception as e:
        print(e, 'problem in test class')
        raise e
    pages_size = len(pages)
    print('num pages', str(len(pages)))
    shared_data.put('pages amount: '+ str(pages_size))
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
            else:
                shared_data.put(str(page.name)[::-1])
                shared_data.put(str(200))

    except Exception as e:
        pass
    finally:
        session.close()
        end_flag.put('end main process')
    print(str(time.time() - start_time))

if __name__ == "__main__":
    main()
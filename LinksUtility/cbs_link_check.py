import requests

from CbsClasses.CbsLink import CbsLink

BUILT_ERROR_MASSAGE = ['Sorry, the page is not found', 'שלום, אנו מצטערים, הגישה לדף זה נחסמה בשל פעולה לא מורשית',
                       'Block ID']
ERROR_PAGES = ["https://www.cbs.gov.il/he/subjects/Pages/%D7%90%D7%95%D7%A1%D7%99%D7%99%D7%94.aspx",
               "https://www.cbs.gov.il/he/subjects/Pages"]

# print(text)
g_link = 'https://httpstat.us/408'


def is_cbs_error_page(content: str):
    error_list: list[str] = []
    for error in BUILT_ERROR_MASSAGE:
        if content.__contains__(error.encode()):
            error_list.append(error)
    if not error_list:
        return False, None
    return True, error_list


def check_cbs_link(new_link: CbsLink, timeout_counter=3):
    while not timeout_counter == 0:
        response = requests.Session()
        try:
            response = requests.get(new_link.link)
            print('no exception')
            break
        except requests.exceptions.Timeout:
            timeout_counter -= 1
            if timeout_counter == 0:
                new_link.status_code = 408
            continue
        finally:
            # if it is one of the cbs error pages set the status_code to 404
            status = is_cbs_error_page(str(response.content))
            if status[0]:
                new_link.status_code = 404
            else:
                new_link.status_code = response.status_code
    return new_link


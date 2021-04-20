import json
import time
from concurrent.futures.thread import ThreadPoolExecutor
import requests
from requests import Session
from selenium import webdriver

from LinksUtility.usefulLinks import Links

u_list = []


def testLinks(session: Session, link):
    res = session.get(link)
    print(res.status_code + '\n')
    res.close()

    # with session.get(link) as response:
    #     print(link + ': ' + response.status_code)
    #     u_list.append((link, response.status_code))

    # try:
    #     r = requests.head(link[0])
    # except Exception as e:
    #     print(e.__cause__)
    # if not r.status_code == 200:
    #     print('not 200')
    # print(link[1], r.status_code)


def main():
    start_time = time.time()

    with open('links.json') as f:
        data = json.load(f)
        f.close()
    l_list = data['links']

    with ThreadPoolExecutor(max_workers=5) as executor:
        with requests.Session() as session:
            executor.map(testLinks, [session] * len(l_list), l_list)
            executor.shutdown(wait=True)
    print(len(l_list))
    print(str(time.time() - start_time))


if __name__ == '__main__':
    main()

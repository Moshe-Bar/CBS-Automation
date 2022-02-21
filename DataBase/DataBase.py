import itertools
import operator

from CbsObjects.CbsLink import CbsLink
from CbsObjects.Converter import Converter
from CbsObjects.Error import Error
from CbsObjects.Pages.SubjectPage import SubjectPage
import pdfkit

import sys
import json
from enum import Enum

####,encoding="utf-8"
from CbsObjects.TestDetails import TestDetails

ROOT_PATH = sys.path[1]

import sqlite3
import sys


class DB:
    def __init__(self):
        self.path = ROOT_PATH + "\\DataBase\\MainDB"
        self.__db = sqlite3.connect(self.path, check_same_thread=False)
        self.__cursor = self.__db.cursor()

    def load_web_parts_dic(self):
        self.__cursor.execute("SELECT * FROM WEB_PARTS_DIC ")
        data = self.__cursor.fetchall()
        return data

    def load_he_subject_pages_dic(self):
        self.__cursor.execute("SELECT * FROM PAGES_DIC WHERE lang='HE' ")
        data = self.__cursor.fetchall()
        return data

    def load_en_subject_pages_dic(self):
        self.__cursor.execute("SELECT * FROM PAGES_DIC WHERE lang='EN' ")
        data = self.__cursor.fetchall()
        return data

    def save_test_results(self, errors):
        insert = "INSERT INTO TEST_RESULTS VALUES (?,?,?,?,?);"
        for i in errors:
            self.__cursor.execute(insert, i.to_list())
        self.__db.commit()
        print('--------------------------------------------------------------')
        print('new {} errors was added successfully to db'.format(len(errors)))
        print('--------------------------------------------------------------')

    def load_test_data(self, test_key):
        select = "SELECT * FROM TEST_RESULTS WHERE test_id=? "
        self.__cursor.execute(select, (test_key,))
        data = self.__cursor.fetchall()
        return data

    def load_errors_dic(self):
        self.__cursor.execute("SELECT * FROM ERRORS_DIC")
        data = self.__cursor.fetchall()
        return data

    def add_new_test(self, details: TestDetails):
        insert = "INSERT INTO TEST_DETAILS VALUES (?,?,?,?,?,?,?);"
        self.__cursor.execute(insert, details.to_list())
        self.__db.commit()

    def __update_new_pages(self, pages):

        index = 400
        insert = "INSERT INTO PAGES_DIC VALUES (?,?,?,?);"

        for page in pages:
            p = [page.name, page.url, index, 'EN']
            if not p[0]:
                p[0] = list(p[1].split('/'))[-1].split('.')[0]
            # en_pages.append(p)
            index += 1
            try:
                self.__cursor.execute(insert, p)
                self.__db.commit()
            except Exception as e:
                print(e)
                print('not inserted: ', p[0], p[1])

    def __del__(self):
        self.__cursor.close()
        self.__db.close()


db = DB()


class DataBase:
    @classmethod
    def get_CBS_he_pages(cls):
        pages = []
        try:
            raw_pages = db.load_he_subject_pages_dic()
            for page in raw_pages:
                link = CbsLink(page_name=page[0], url=page[1])
                pages.append(SubjectPage(link, page[0], id=page[2], lang=page[3]))
        except Exception as e:
            print('database exception, can not load pages dict', e)
            raise e
        pages = list(set(pages))
        excluded = ('/search/', '/Surveys/', '/Documents/', '/publications/')
        pages = list(filter(lambda x: all(s not in x.link.url for s in excluded), pages))
        pages.sort(key=lambda x: x.name)
        return pages

    @classmethod
    def get_CBS_en_pages(cls):
        pages = []
        try:
            raw_pages = db.load_en_subject_pages_dic()
            for page in raw_pages:
                link = CbsLink(page_name=page[0], url=page[1])
                pages.append(SubjectPage(link, page[0], id=page[2], lang=page[3]))
        except Exception as e:
            print('database exception, can not load pages dict', e)
            raise e
        pages = list(set(pages))
        excluded = ('/search/', '/Surveys/', '/Documents/', '/publications/')
        pages = list(filter(lambda x: all(s not in x.link.url for s in excluded), pages))
        pages.sort(key=lambda x: x.name)
        return pages

    @classmethod
    def save_test_results(cls, test_key, page: SubjectPage):
        try:
            errors = page.get_errors()
            for error in errors:
                error.test_id = test_key
            db.save_test_results(errors)

        except Exception as e:
            print('exception in db new db insertion')
            raise e

    @classmethod
    def get_test_results(cls, test_key):
        try:
            return db.load_test_data(test_key)
        except Exception as e:
            print("exception in db, couldn't load test results")
            raise e

    @classmethod
    def load_xpath(cls, key):
        with open(ROOT_PATH + '\\Configuration\\xpath.json', 'rb') as f:
            data = json.load(f)
            f.close()
        return data['XPath'][0][key]

    @classmethod
    def get_webdriver_path(cls):
        with open(ROOT_PATH + '\\Configuration\\webdriver_path.json', 'rb') as file:
            data = json.load(file)
            file.close()
        return data['driver_path']

    @classmethod
    def get_pdf_test_results(cls, test_ID):
        data = cls.get_test_results(test_ID)
        return Converter.to_pdf(data)

    @classmethod
    def init_new_test(cls, test_details):
        db.add_new_test(test_details)

    @classmethod
    def get_excel_test_results(cls, test_ID):
        data = cls.get_test_results(test_ID)
        Converter.to_excel(data)


class Links(Enum):
    CBS_HOME_PAGE_HE = 'https://www.cbs.gov.il/he/Pages/default.aspx'
    CBS_MAP_SITE_HE = 'https://www.cbs.gov.il/he/pages/sitemap.aspx'
    CBS_MAP_SITE_EN = 'https://www.cbs.gov.il/en/Pages/sitemap.aspx'
    ROOT_XPATH = DataBase.load_xpath('ROOT_XPATH')
    ROOT_DIR = sys.path[1]
    CHROME_DRIVER = ROOT_DIR + "/" + DataBase.get_webdriver_path()
    HEBREW_STATS_XPATH = DataBase.load_xpath('HEBREW_STATS_XPATH')
    RIGHT_EXTRA_PARTS_XPATH = DataBase.load_xpath('RIGHT_EXTRA_PARTS_XPATH')
    LEFT_EXTRA_PARTS_XPATH = DataBase.load_xpath('LEFT_EXTRA_PARTS_XPATH')
    TOOLS_AND_DB_XPATH = DataBase.load_xpath('TOOLS_AND_DB_XPATH')
    SUMMARY_XPATH = DataBase.load_xpath('SUMMARY_XPATH')
    TOP_BOX_XPATH = DataBase.load_xpath('TOP_BOX_XPATH')
    SUB_SUBJECTS_XPATH = DataBase.load_xpath('SUB_SUBJECTS_XPATH')
    PRESS_RELEASES_XPATH = DataBase.load_xpath('PRESS_RELEASES_XPATH')
    TABLES_AND_CHARTS_XPATH = DataBase.load_xpath('TABLES_AND_CHARTS_XPATH')
    PUBLICATIONS_XPATH = DataBase.load_xpath('PUBLICATIONS_XPATH')
    GEOGRAPHIC_ZONE_XPATH = DataBase.load_xpath('GEOGRAPHIC_ZONE_XPATH')
    INTERNATIONAL_COMPARISONS_XPATH = DataBase.load_xpath('INTERNATIONAL_COMPARISONS_XPATH')  # new
    MORE_LINKS_XPATH = DataBase.load_xpath('MORE_LINKS_XPATH')  # new
    CONFERENCES_AND_SEMINARS_XPATH = DataBase.load_xpath('CONFERENCES_AND_SEMINARS_XPATH')  # new
    VIDEOS_LINKS_XPATH = DataBase.load_xpath('VIDEOS_LINKS_XPATH')  # new
    PICTURES_LINKS_XPATH = DataBase.load_xpath('PICTURES_LINKS_XPATH')  # new
    PRESENTATIONS_XPATH = DataBase.load_xpath('PRESENTATIONS_XPATH')  # new



DataBase.get_excel_test_results('''cda22bde-b903-4f37-8a4f-507fc9a1618e''')
# file = ROOT_PATH + '\\DataBase\\to_pdf.pdf'
# with open(file,'wb') as f:
#     f.write(bytes(data))
#     f.close()
# #######
# links = list(set(DataBase.get_CBS_en_links()))
#
# print(links)
# db.update_new_pages(links)
###########

# st =  'https://www.cbs.gov.il/en/subjects/Pages/Index-of-Compactness-of-Municipalities-and-Local-Councils.aspx'
# print(st.split('/')[-1].split('.')[0])
# x = DB()
# # print(x.get_he_subject_pages())
# x.add_new_test([0, 1, 2, 3])
# print(sys.path[1]+"\\DL\\DB\\")
# driver = TestUtility.get_sessions()[0]
# driver.get('https://getsharex.com/')
#
# print(Links.ROOT_XPATH.value)
# summ = [1,2,3,4,5]
# path = '02_Jun_2021_10.48.50'
# DataBase.save_summary_result(file_key=path,summery=summ)
# print(DataBase.get_CBS_he_pages()[30])


# @classmethod
# def save_test_result(cls, test_key, page: SubjectPage):
#     try:
#         path = ROOT_PATH + '\\TestData\\logs'
#         file = path + '\\' + test_key + '.html'
#         with open(file, 'a', encoding='utf-8') as f:
#             style = 'style={color:red; font-size: large; }'
#             page_link = '<h1 {}><a style="color:red" href="{}" target="_blank" >{}</a></h1><br>'.format(style,
#                                                                                                         page.link.url,
#                                                                                                         page.name)
#             errors = ('<h1 {}>' + str(page.error_to_str()) + '</h1><br>').format(style)
#             f.write(page_link + errors)
#         f.close()
#     except Exception as e:
#         print('exception in db')
#         raise e

# @classmethod
#     def save_summary_result(cls, file_key, summary):
#         sum = '<h1 style="color:black" style={color:red; font-size: large; }>Test started on: ' + str(
#             summary[0]) + ' ' + str(summary[1]) + '<br>'
#         sum += 'Total pages: ' + str(summary[2]) + '<br>'
#         sum += 'Tested: ' + str(summary[3]) + '<br>'
#         sum += 'Total error pages: ' + str(summary[4]) + '</h1>'
#         file_name = file_key
#         head = '''<!DOCTYPE html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <title>Title</title>
#         </head>
#         <body>'''
#         tail = '</body></html>'
#
#         try:
#             path = ROOT_PATH + '\\TestData\\logs'
#             file = path + '\\' + file_name + '.html'
#             with open(file, 'r', encoding='utf-8') as f:
#                 content = f.read()
#                 f.close()
#             with open(file, 'w', encoding='utf-8') as f:
#                 f.write(head + sum + '<br>' + content + tail)
#             f.close()
#         except Exception as e:
#             print('exception in db writing summery')
#             raise e

from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
import pdfkit


import sys
import json
from enum import Enum

####,encoding="utf-8"
ROOT_PATH = sys.path[1]


class DataBase:
    @classmethod
    def get_CBS_he_links(cls):
        links = []
        try:
            with open(ROOT_PATH + '\\DataBase\\heb_pages_links.txt', 'r', encoding="utf-8") as f:
                for line in f:
                    li = line.split()
                    cbs_link = CbsLink(li[0])
                    cbs_link.name = ' '.join(li[1:])
                    links.append(cbs_link)
                f.close()
        except Exception as e:
            print(e)
            print('database file did not read', e)
        links = list(set(links))
        excluded = ('/search/', '/Surveys/', '/Documents/', '/publications/')
        links = list(filter(lambda x: all(s not in x.url for s in excluded), links))
        links.sort(key=lambda x: x.name)
        return links

    @classmethod
    def get_CBS_he_links_db(cls):
        # todo
        pass

    @classmethod
    def get_CBS_en_links(cls):
        links = []
        try:
            with open(ROOT_PATH + '\\DataBase\\en_pages_links.txt', 'r', encoding="utf-8") as f:
                for line in f:
                    li = line.split()
                    cbs_link = CbsLink(li[0])
                    cbs_link.name = ' '.join(li[1:])
                    links.append(cbs_link)
                f.close()
        except Exception as e:
            print(e)
            print('database file did not read', e)
        return links

    @classmethod
    def get_CBS_he_pages(cls):
        links = cls.get_CBS_he_links()  # the links only saved locally
        pages = [SubjectPage(link, link.name, i + 1) for i, link in enumerate(links)]

        # pages = list(map(lambda link:SubjectPage(link, link.name,),links))
        # pages = [SubjectPage(link, link.name,) for i,link in links]
        return pages

    @classmethod
    def get_CBS_en_pages(cls):
        links = cls.get_CBS_en_links()
        pages = [SubjectPage(link, link.name) for link in links]
        return pages

    @classmethod
    def save_test_result(cls, test_key, page: SubjectPage):
        try:
            path = ROOT_PATH + '\\TestData\\logs'
            file = path + '\\' + test_key + '.html'
            with open(file, 'a', encoding='utf-8') as f:
                style = 'style={color:red; font-size: large; }'
                page_link = '<h1 {}><a style="color:red" href="{}" target="_blank" >{}</a></h1><br>'.format(style,
                                                                                                            page.link.url,
                                                                                                            page.name)
                errors = ('<h1 {}>' + str(page.error_to_str()) + '</h1><br>').format(style)
                f.write(page_link + errors)
            f.close()
        except Exception as e:
            print('exception in db')
            raise e

    @classmethod
    def get_test_result(cls, file_key):

        file_name = file_key
        try:
            path = ROOT_PATH + '\\TestData\\logs'
            file = path + '\\' + file_name + '.html'

            with open(file, 'r', encoding='utf-8') as f:
                data = f.read()
                f.close()

            # with open(file, 'w', encoding='utf-8') as f:
            #     f.write(head + data + tail)
            #     f.close()
            #
            # with open(file, 'r', encoding='utf-8') as f:
            #     data = f.read()
            #     f.close()

            return data, file
        except Exception as e:
            print('exception in db reading file content')
            raise e

    @classmethod
    def save_summary_result(cls, file_key, summary):
        sum = '<h1 style="color:black" style={color:red; font-size: large; }>Test started on: ' + str(
            summary[0]) + ' ' + str(summary[1]) + '<br>'
        sum += 'Total pages: ' + str(summary[2]) + '<br>'
        sum += 'Tested: ' + str(summary[3]) + '<br>'
        sum += 'Total error pages: ' + str(summary[4]) + '</h1>'
        file_name = file_key
        head = '''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>'''
        tail = '</body></html>'

        try:
            path = ROOT_PATH + '\\TestData\\logs'
            file = path + '\\' + file_name + '.html'
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                f.close()
            with open(file, 'w', encoding='utf-8') as f:
                f.write(head + sum + '<br>' + content+ tail)
            f.close()
        except Exception as e:
            print('exception in db writing summery')
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
    def get_pdf_test_result(cls, file_key):
        data,file_path = cls.get_test_result(file_key)
        # data,is_success = pdfkit.from_file('test.html', 'out.pdf')
        data = pdfkit.from_string(data)
        return data


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

# import sqlite3
# import sys
#
#
# class DB:
#     def __init__(self):
#         self.path = sys.path[1]+"\\DL\\DB\\"
#         self.__db = sqlite3.connect(self.path + 'pagesDB')
#         self.__cursor = self.__db.cursor()
#
#     def get_he_links(self):
#         self.__cursor.execute("SELECT * FROM addresses")
#         data = self.__cursor.fetchall()
#         return data
#
#     def get_wp_ids(self):
#         self.__cursor.execute("SELECT * FROM WPARTS")
#         data = self.__cursor.fetchall()
#         return data
#
#     def save_test_result(self, row_data):
#         insert = "INSERT INTO TEST_RESULT VALUES ({},{},{},{},{});"
#         self.__cursor.executescript(insert.format(*row_data))
#         self.__cursor.fetchall()
#
#     def load_test_data(self, test_key):
#         pass
#
#     def load_error_details(self):
#         self.__cursor.execute("SELECT * FROM ERRORS")
#         data = self.__cursor.fetchall()
#         return data
#
#     def add_new_test(self,details):
#         insert = "INSERT INTO TEST_DETAILS VALUES ({},{},{},{});"
#         self.__cursor.executescript(insert.format(*details))
#         self.__cursor.fetchall()

# x = DB()
# x.save_test_result([0,1,2,3,4])
# print(sys.path[1]+"\\DL\\DB\\")
# driver = TestUtility.get_sessions()[0]
# driver.get('https://getsharex.com/')

# print(Links.ROOT_XPATH.value)
# summ = [1,2,3,4,5]
# path = '02_Jun_2021_10.48.50'
# DataBase.save_summary_result(file_key=path,summery=summ)
# print(DataBase.get_CBS_he_pages()[30])

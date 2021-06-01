import time

import xlsxwriter

# workbook = xlsxwriter.Workbook('hello.xlsx')
# worksheet = workbook.add_worksheet()
#
# worksheet.write('A1', 'Hello world')
# # a = 'A'
# # print(chr(ord(a)+ 1))
#
# workbook.close()
# print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
from CbsObjects.CbsLink import CbsLink
from CbsObjects.Pages.SubjectPage import SubjectPage
from dataBase.DataBase import DataBase

# print(time.strftime("%d %b %Y %H.%M.%S", time.gmtime()).replace(' ', '_'))
# test = 'https://www.w3schools.com/python/ref_string_replace.asp'
# DataBase.save_test_result(time.strftime("%d %b %Y %H.%M.%S", time.gmtime()).replace(' ', '_'),
#                           SubjectPage(CbsLink(test), 'test'))
print(DataBase.get_test_result('01_Jun_2021_07.08.48'))
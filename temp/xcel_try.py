import datetime
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
from DL.DataBase import DataBase
# local_page = SubjectPage(CbsLink(r'D:\Current\Selenium\NewAutomationEnv\DataBase\local\נושאים - רווחת האוכלוסייה ועמדות כלפי שירותי ממשל 2007.html'),'local page')

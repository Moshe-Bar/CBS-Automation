from CbsObjects import CbsLink
from CbsObjects.WebParts import WebPart


class WebPartLine:

    def __init__(self, url, pic, index, date=None, name=None):
        self.__index = index
        self.__url: CbsLink = url
        self.__pic_url: CbsLink = pic
        self.__date = date
        self.__name = name

    @property
    def url(self):
        return self.__url

    @property
    def pic(self):
        return self.__pic_url

    @property
    def date(self):
        return self.__date

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return 'Line {}: {}'.format(self.__index, self.__name)


# a = WebPartLine('www.klum.com','www.klum.com.klum.png','tables and charts',1,name='link')
# print(a)
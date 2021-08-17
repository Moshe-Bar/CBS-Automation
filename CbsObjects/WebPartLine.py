from CbsObjects import CbsLink


class WebPartLine:

    def __init__(self, url, pic, date):
        self.__url: CbsLink = url
        self.__pic_url: CbsLink = pic
        self.__date = date

    @property
    def url(self):
        return self.__url

    @property
    def pic(self):
        return self.__pic_url

    @property
    def date(self):
        return self.__date




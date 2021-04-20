from CbsClasses.CbsLink import CbsLink
from cbsPage.Language import Language


class CbsPage:
    def __init__(self, pageLink, pageName):
        self.link = CbsLink(pageLink)
        self.name = pageName
        self.level = None
        self.parent = None
        self.children = []
        self.lang = Language.HEBREW.value
        self.web_parts = []

    def __iter__(self):
        return iter(self.web_parts)

    def __next__(self):
        return next(self.web_parts)

    def get_level(self):
        return self.level

    def get_link(self):
        return self.link

    def __str__(self):
        return self.name + '::' + str(self.link.status_code)

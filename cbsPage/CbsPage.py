from cbsPage.Language import Language

class CbsPage:
    def __init__(self, pageLink, pageName,pageLevel):
        self.link = pageLink
        self.name = pageName
        self.level = pageLevel
        self.parent = CbsPage('0', '0')
        self.children = []
        self.iterationIndex = 0
        self.lang = Language
        
    def __iter__(self):
        pass

    def __next__(self):
        raise StopIteration

    def getLevel(self):
        pass

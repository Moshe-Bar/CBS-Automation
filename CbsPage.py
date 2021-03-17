class CbsPage:
    def __init__(self, link, name,level):
        self.link = link
        self.name = name
        self.level = level
        self.parenet = CbsPage('0', '0')
        self.children = []
        self.iterationIndex = 0
        self.lang = 'HE'

    def __iter__(self):
        pass

    def __next__(self):
        raise StopIteration

    def getLevel(self):
        pass

class CbsLink:
    def __init__(self, link_text):
        self.link = link_text
        self.status_code = None
        self.name = None
        self.language = None
        self.type = None

    def __str__(self):
        return self.status_code + '::' + self.link


class CbsLinks:
    def __init__(self):
        self.links: list[CbsLink] = []

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.links):
            self.index += 1
            return self.links[self.index]
        else:
            raise StopIteration



    def append(self, link):
        self.links.append(link)

from CbsObjects.CbsLink import CbsLink


class ImgTag:
    def __init__(self, url):
        self.url = url


class ATag:
    def __init__(self, url, text=None, img=None):
        self.img = img
        self.url: CbsLink = url
        self.text = text


class Componenet:
    def __init__(self, a_tag_list: [ATag], img: ImgTag = None, date=None):
        self.date = date
        self.a_tags: [ATag] = a_tag_list
        self.img_tag = img

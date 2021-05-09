class CbsLink:
    def __init__(self, url, page_name= None):
        self.url = url
        self.status_code = None
        self.name = page_name
        self.language = None
        self.type = None

    def get_url(self):
        return self.url

    def __str__(self):
        return str(self.status_code) + '::' + self.url

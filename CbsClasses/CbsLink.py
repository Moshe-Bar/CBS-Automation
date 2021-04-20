class CbsLink:
    def __init__(self, url):
        self.url = url
        self.status_code = None
        self.name = None
        self.language = None
        self.type = None

    def get_url(self):
        return self.url

    def __str__(self):
        return str(self.status_code) + '::' + self.url




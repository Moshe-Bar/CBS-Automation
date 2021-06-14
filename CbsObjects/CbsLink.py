class CbsLink:
    def __init__(self, url:str, page_name= None):
        self.url = url
        self.status_code = None
        self.name = page_name
        self.language = None
        self.type = self.get_type(url)

    def get_url(self):
        return self.url

    def __str__(self):
        return str(self.status_code) + '::' + self.url

    def get_type(self, url):

        if url.endswith('.aspx'):
            self.type = 'aspx'
        elif url.endswith('.pdf'):
            self.type = 'pdf'
        elif url.endswith('.excel'):
            self.type = 'excel'
page_files = ('html', 'aspx')


class CbsLink:
    def __init__(self, url: str, page_name=None):
        self.url = url
        self.status_code = None
        self.name = page_name
        self.file_type = self.url.split('.')[-1]
        self.type = None
        if any(self.url.endswith(s) for s in page_files):
            self.type = 'page'
        else:
            self.type = 'file'

    def __str__(self):
        return str(self.status_code) + '::' + self.url + '::' + self.name

    def __eq__(self, other):
        return self.url.__eq__(other.url)

    def __hash__(self):
        return hash(self.name)



class CbsLink:
    def __init__(self, url:str, page_name= None):
        self.url = url
        self.status_code = None
        self.name = page_name
        self.file_type = self.url.split('.')[-1]

    def __str__(self):
        return str(self.status_code) + '::' + self.url + '::' + self.name




# url = 'https://www.cbs.gov.il/he/subjects/Pages/%D7%A8%D7%95%D7%95%D7%97%D7%AA-%D7%94%D7%90%D7%95%D7%9B%D7%9C%D7%95%D7%A1%D7%99%D7%99%D7%94-%D7%95%D7%A2%D7%9E%D7%93%D7%95%D7%AA-%D7%9B%D7%9C%D7%A4%D7%99-%D7%A9%D7%99%D7%A8%D7%95%D7%AA%D7%99-%D7%9E%D7%9E%D7%A9%D7%9C-2007.aspx'
# url = ''
# print(url.split('.')[-1])

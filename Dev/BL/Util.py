from Dev.DL.DBAdapter import DBAdapter
from CbsObjects.Page import SubjectPage



class Util:
    def __init__(self):
        self.__db = DBAdapter()

    # returns array of SubjectPages
    def get_pages(self,lang='he'):
        raw_pages = self.__db.get_CBS_he_links()
        return [SubjectPage(pageName=p[0],pageLink=p[1],pageID=p[2]) for p in raw_pages]



x=Util()
print('len: ',len(x.get_pages()),'first: ',x.get_pages()[1])
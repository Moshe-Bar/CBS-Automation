from CbsObjects.CbsLink import CbsLink
from CbsObjects.WebParts import Statisticals, SubSubjects, MoreLinks, SPWebParts, PressReleases
from CbsObjects.Language import Language


class SubjectPage:
    class WebParts:
        def __init__(self):
            self.stats_part = Statisticals()
            self.sub_subjects = SubSubjects()
            self.more_links = MoreLinks()

    def __init__(self, pageLink: CbsLink, pageName):
        self.link = pageLink
        self.name = pageName
        self.level = None
        self.parent = None
        self.children = []
        self.lang = None
        self.web_parts = SPWebParts()
        self.stats_part = Statisticals()
        self.sub_subjects = SubSubjects()
        self.press_releases = PressReleases()
        self.more_links = MoreLinks()
        self.inside_links = []
        self.dom = None
        self.isChecked = None

    def isCorrect(self):
        return len(self.get_errors()) == 0

    def get_errors(self):
        # errors = [str(part.errors) + ('\n') for part in self.web_parts]
        # return errors
        return self.stats_part.errors + self.press_releases.errors
    
    def __iter__(self):
        return iter(self.inside_links)

    def __next__(self):
        return next(self.inside_links)

    def get_level(self):
        return self.level

    def get_link(self):
        return self.link

    def set_inside_links(self, links: [CbsLink]):
        self.inside_links.extend(links)

    def __len__(self):
        return len(self.inside_links)

    def __str__(self):
        return self.name



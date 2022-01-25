from CbsObjects.CbsLink import CbsLink
from CbsObjects.Error import Error
from CbsObjects.WebParts import Statisticals, SubSubjects, MoreLinks, ToolsAndDB, Summary, TopBox, \
    PressReleases, TablesAndMaps, ExParts, Publications, GeographicZone, InternationalComparisons, Presentations


class SubjectPage:

    def __init__(self, pageLink: CbsLink, pageName,id=None):
        self.link = pageLink
        self.name = pageName
        self.level = None
        self.parent = None
        self.children = []
        self.lang = None
        self.__web_parts = {
            'stats_part': Statisticals(),
            'sub_subjects': SubSubjects(),
            'tools_and_db': ToolsAndDB(),
            'more_links': MoreLinks(),
            'summary': Summary(),
            'top_box': TopBox(),
            'press_releases': PressReleases(),
            'tables_and_charts': TablesAndMaps(),
            'extra_error_parts': ExParts(),
            'publications': Publications(),
            'geographic_zone': GeographicZone(),
            'international_comparisons':InternationalComparisons(),
            'presentations':Presentations()
        }
        self.inside_links = []
        self.dom = None
        self.isChecked = None
        self.id = id

    @property
    def stats_part(self):
        return self.__web_parts['stats_part']

    # @stats_part.setter

    @property
    def sub_subjects(self):
        return self.__web_parts['sub_subjects']

    @property
    def tools_and_db(self):
        return self.__web_parts['tools_and_db']

    @property
    def more_links(self):
        return self.__web_parts['more_links']

    @property
    def summary(self):
        return self.__web_parts['summary']

    @property
    def top_box(self):
        return self.__web_parts['stats_part']

    @property
    def press_releases(self):
        return self.__web_parts['press_releases']

    @property
    def tables_and_charts(self):
        return self.__web_parts['tables_and_charts']

    @property
    def extra_error_parts(self):
        return self.__web_parts['extra_error_parts']

    @property
    def publications(self):
        return self.__web_parts['publications']

    @property
    def geographic_zone(self):
        return self.__web_parts['geographic_zone']

    @property
    def international_comparisons(self):
        return self.__web_parts['international_comparisons']

    @property
    def presentations(self):
        return self.__web_parts['presentations']

    def isCorrect(self):
        return len(self.get_errors()) == 0

    def get_errors(self):
        errors = []
        for web_part in self.__web_parts.values():
            err = web_part.get_errors()
            for e in err:
                e.page_id = self.id
                errors.append(e)
            # if len(err) > 0:
            #     errors.append(err)
        return errors
        # return [web_part.get_errors() for web_part in self.__web_parts.values()]

    def error_to_str(self):
        s=''
        for e in self.get_errors():
            s = s + ', ' + str(e)
        return s
        # errors = []
        # for web_part in self.__web_parts.values():
        #     err = web_part.get_errors()
        #     if len(err) > 0:
        #         errors.append(web_part.error_to_str())
        # return '\n'.join(errors)
        # return '\n'.join([web_part.error_to_str() for web_part in self.__web_parts.values()])

    def get_level(self):
        return self.level

    def get_link(self):
        return self.link

    def set_inside_links(self, links: [CbsLink]):
        self.inside_links.extend(links)

    def __len__(self):
        return len(self.inside_links)

    def __str__(self):
        return 'Name: {}, ID: {}'.format(self.name,self.id)


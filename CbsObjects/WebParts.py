from abc import ABC, abstractmethod

# from dataBase.DataBase import Links


class CbsWebPart(ABC):
    pass
    # @abstractmethod
    # @classmethod
    # def getXPATH(cls):
    #     pass


# תקציר בראש הדף
class Summary(CbsWebPart):
    def __init__(self):
        self.errors = []
        self.images = []
        self.links = []

    @classmethod
    def getXPATH(cls):
        pass
        # return Links.SUMMERY_XPATHS.value

# רגע של סטטיסטיקה
class MomentOfStatistics(CbsWebPart):
    def xPath(self):
        pass

    def getDetails(self):
        pass

    def __init__(self):
        super().__init__()

    def isShowed(self):
        pass

    def isWorkingProperly(self):
        pass


# שלושת המלבנים
class TopLinksBox(CbsWebPart):
    def __init__(self):
        self.errors = []
        self.images = []
        self.links = []

    @classmethod
    def getXPATH(cls):
        return None

# מידע לפי אזור גיאוגרפי
class GeographicZone(CbsWebPart):
    pass


# השוואות בינ"ל
class InternationalComparisons(CbsWebPart):
    pass


# עלוני סטטיסטיקל
class Statisticals(CbsWebPart):
    def __init__(self):
        self.errors = []
        self.good_condition = True
        self.isHidden = None
        self.images = []
        self.links = []


    def isShowed(self):
        return not self.isHidden

    def isWorkingProperly(self):
        return self.good_condition

    def getDetails(self):
        return self.errors

    @classmethod
    def getXPATH(cls):
        pass
        # return Links.HEBREW_STATS_XPATH.value


# class ExtraStatisticals(CbsWebPart):
#     def __init__(self):
#         self.errors = []
#         self.good_condition = True
#         self.isHidden = None
#         self.images = []
#         self.links = []
#
#     def set_hidden(self, isHidden: bool):
#         self.isHidden = isHidden
#         if not isHidden:
#             self.errors.append('extra stats are showed')
#             self.good_condition = False
#
#     def isShowed(self):
#         return not self.isHidden
#
#     def isWorkingProperly(self):
#         return self.good_condition
#
#     def getDetails(self):
#         return self.errors
#
#     def xPath(self):
#         pass


# נושאי משנה
class SubSubjects(CbsWebPart):
    def __init__(self):
        self.errors = []
        self.good_condition = True
        self.isHidden = None
        self.images = []
        self.links = []

    def isShowed(self):
        return not self.isHidden

    def isWorkingProperly(self):
        if len(self.errors) == 0:
            return True
        return False

    def getDetails(self):
        return self.errors

    def xPath(self):
        pass


# הודעות לתקשורת
class PressReleases(CbsWebPart):
    def __init__(self):
        self.errors = []
        self.good_condition = True
        self.isHidden = None

    def set_hidden(self, isHidden: bool):
        self.isHidden = isHidden
        if not isHidden:
            self.errors.append('extra press releases is showed')
            self.good_condition = False

    def isShowed(self):
        return not self.isHidden

    def isWorkingProperly(self):
        return self.good_condition

    def getDetails(self):
        return self.errors

    def xPath(self):
        pass


# לוחות ותרשימים
class TableMaps(CbsWebPart):
    pass


class MoreLinks(CbsWebPart):
    def __init__(self):
        self.errors = []
        self.isHidden = None
        self.images = []
        self.links = []

    def isShowed(self):
        return not self.isHidden

    def isWorkingProperly(self):
        if len(self.errors) == 0:
            return True
        return False

    def getDetails(self):
        return self.errors

    def xPath(self):
        pass


# collection of web parts
class SPWebParts:
    def __init__(self):
        parts = []
        self.statistical: Statisticals()
        self.more_links = MoreLinks()
        self.sub_subjects = SubSubjects()
        self.summery = Summary()
        self.mom_of_statistics = MomentOfStatistics()
        self.top_links_box = TopLinksBox()
        self.geo_zone = GeographicZone()
        self.international_comparisons = InternationalComparisons()
        self.press_releases = PressReleases()
        self.tables_and_maps = TableMaps()


    def __len__(self):
        return 11

    def __next__(self):
        pass

    def __iter__(self):
        pass

    # def get_summary(self):
    #     return 10


# a = SPWebParts()
# print(a.summery)


class ExParts():
    def __init__(self):
        self.errors = []
        self.good_condition = True
        self.isHidden = None


class ToolsAndDB:
    def __init__(self):
        self.errors = []
        self.good_condition = True
        self.isHidden = None
        self.images = []
        self.links = []

    def set_errors(self, error):
        self.errors.append(error)
        self.good_condition = False

    def isShowed(self):
        return not self.isHidden

    def isWorkingProperly(self):
        return self.good_condition

    def getDetails(self):
        return self.errors

    def xPath(self):
        pass

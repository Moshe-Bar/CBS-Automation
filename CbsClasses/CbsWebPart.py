from abc import ABC, abstractmethod


class CbsWebPart(ABC):

    def __int__(self):
        self.errors = []
        self.good_condition = True
        self.isHidden = None
        self.images = []
        self.links = []

    @abstractmethod
    def isShowed(self):
        pass

    @abstractmethod
    def isWorkingProperly(self):
        return self.good_condition

    @abstractmethod
    def getDetails(self):
        pass

    @abstractmethod
    def xPath(self):
        pass


# תקציר בראש הדף
class Summary(CbsWebPart):
    def xPath(self):
        return "//div[@class = 'rightColumn']//div[@class = 'textBox borderBottom transBox']//p//a[@href]"

    def getDetails(self):
        pass

    def __init__(self):
        super().__init__()

    def isShowed(self):
        pass

    def isWorkingProperly(self):
        return self.condition


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
    pass


# נידע לפי אזור גיאוגרפי
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


class ExtraStatisticals(CbsWebPart):
    def __init__(self):
        self.errors = []
        self.good_condition = True
        self.isHidden = None
        self.images = []
        self.links = []

    def set_hidden(self,isHidden:bool):
        self.isHidden = isHidden
        if not isHidden:
            self.errors.append('extra stats are showed')
            self.good_condition = False

    def isShowed(self):
        return not self.isHidden

    def isWorkingProperly(self):
        return self.good_condition

    def getDetails(self):
        return self.errors

    def xPath(self):
        pass

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
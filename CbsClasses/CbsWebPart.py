from abc import ABC, abstractmethod
from CbsClasses.CbsLink import CbsLink


class CbsWebPart(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def isShowed(self):
        pass

    @abstractmethod
    def isWorkingProperly(self):
        pass

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
        pass


# רגע של סטטיסטיקה
class MomentOfStatistics(CbsWebPart):
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
    pass


# נושאי משנה
class SubSubjects(CbsWebPart):
    pass


# הודעות לתקשורת
class PressReleases(CbsWebPart):
    pass


# לוחות ותרשימים
class TableMaps(CbsWebPart):
    pass

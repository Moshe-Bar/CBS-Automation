from abc import ABC, abstractmethod

from CbsObjects import Component
from CbsObjects.WebPartLine import WebPartLine


class WebPart():
    def __init__(self):
        self.title = None
        self.components = [Component]
        self.errors = []
        self.images = []
        self.links = []
        self.lines = [WebPartLine]

    def get_errors(self):
        return self.errors

    def error_to_str(self):
        return ', '.join(self.errors)


# תקציר בראש הדף
class Summary(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'Summary: ' + super().error_to_str()


# רגע של סטטיסטיקה
class MomentOfStatistics(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'Moment Of Statistics: ' + super().error_to_str()


# שלושת המלבנים
class TopBox(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'Top Box: ' + super().error_to_str()


# מידע לפי אזור גיאוגרפי
class GeographicZone(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'Geographic Zone: ' + super().error_to_str()


# השוואות בינ"ל
class InternationalComparisons(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'International Comparisons: ' + super().error_to_str()


# עלוני סטטיסטיקל
class Statisticals(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'Statisticals: ' + super().error_to_str()


# נושאי משנה
class SubSubjects(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'Sub Subjects: ' + super().error_to_str()


# הודעות לתקשורת
class PressReleases(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'Press Releases: ' + super().error_to_str()


# לוחות ותרשימים
class TablesAndMaps(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'Tables And Maps: ' + super().error_to_str()


class MoreLinks(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'More Links: ' + super().error_to_str()


class ExParts(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'Extra Error Parts: ' + super().error_to_str()


class ToolsAndDB(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'Tools And DataBase: ' + super().error_to_str()

class Publications(WebPart):
    def __init__(self):
        super().__init__()

    def error_to_str(self):
        return 'Publications: ' + super().error_to_str()
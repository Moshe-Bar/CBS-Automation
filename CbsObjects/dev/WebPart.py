class Errors(list):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return None

class WebPart:

    def __init__(self):
        self.title = None
        self.text = None
        self.free_images = None
        self.components = []
        self.errors = Errors()

    def get_errors(self):
        return self.errors


# תקציר בראש הדף
class Summary(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'Summary: ' + str(super().get_errors())


# רגע של סטטיסטיקה
class MomentOfStatistics(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'Moment Of Statistics: ' + super().get_errors()


# שלושת המלבנים
class TopBox(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'Top Box: ' + super().get_errors()


# מידע לפי אזור גיאוגרפי
class GeographicZone(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'Geographic Zone: ' + super().get_errors()


# השוואות בינ"ל
class InternationalComparisons(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'International Comparisons: ' + super().get_errors()


# עלוני סטטיסטיקל
class Statisticals(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'Statisticals: ' + super().get_errors()


# נושאי משנה
class SubSubjects(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'Sub Subjects: ' + super().get_errors()


# הודעות לתקשורת
class PressReleases(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'Press Releases: ' + super().get_errors()


# לוחות ותרשימים
class TablesAndMaps(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'Tables And Maps: ' + super().get_errors()


class MoreLinks(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'More Links: ' + super().get_errors()


class ExParts(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'Extra Error Parts: ' + super().get_errors()


class ToolsAndDB(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'Tools And DataBase: ' + super().get_errors()


class Publications(WebPart):
    def __init__(self):
        super().__init__()

    def get_errors(self):
        return 'Publications: ' + super().get_errors()

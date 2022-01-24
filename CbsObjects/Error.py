from enum import Enum


class Error:
    def __init__(self, error_type, wp_type=None, index=None):
        self.type = error_type
        self.wp_type = wp_type
        self.index = index
        self.page_id = None
        self.test_id = None

    def __repr__(self):
        return [self.test_id, self.page_id, self.wp_type, self.type, self.index]


class Type(Enum):
    TITLE_NOT_CORRECT = 0
    WRONG_WP_ON_LEFT_SIDE = 1
    WRONG_WP_ON_RIGHT_SIDE = 2
    IMAGES_OR_LINKS_ARE_MISSING = 3
    TO_ALL_MASSAGES_IS_MISSING = 4
    BROKEN_IMAGE_LINK = 5
    BROKEN_LINK = 6
    MISSING_TEXT = 7
    MISSING_IMAGES=8
    MISSING_LINKS=9
    TO_ALL_MASSAGES_IS_BROKEN = 10
    NO_CONTENT = 11

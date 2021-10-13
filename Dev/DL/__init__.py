from Config import Config
from DB import DB


class Adapter():
    @classmethod
    def get_xpath(cls):
        return Config.get_xpath()

    @classmethod
    def get_driver_path(cls):
        return Config.get_driver()

    @classmethod
    def get_he_links(cls):
        return DB().get_he_links()

    @classmethod
    def save_test_data(cls, test_key, test_data):
        DB().save_test_result(test_key, test_data)

    @classmethod
    def get_test_data(cls,test_key):
        return DB().load_test_data(test_key)

from CbsClasses.CbsPageUtility import CbsPageUtility


class TestUtility:
    @classmethod
    def initial_test_environment(cls, wait_time=10):
        session = CbsPageUtility.create_web_driver(wait_time)
        pages = CbsPageUtility.get_cbs_map_pages()
        return session, pages

    @classmethod
    def test_web_parts(cls, statistical=False):
        pass
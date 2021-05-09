from Testing.TestUtility import TestUtility


def main():
    pages = TestUtility.get_pages()
    TestUtility.test(pages=pages, session_visible=False)


if __name__ == "__main__":
    main()

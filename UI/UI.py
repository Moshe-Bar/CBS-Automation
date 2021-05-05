from Testing.TestUtility import TestUtility





def main():
    pages = TestUtility.get_pages()
    TestUtility.test(pages=pages)

if __name__ == "__main__":
    main()

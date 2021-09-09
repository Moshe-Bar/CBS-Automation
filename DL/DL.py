# Singleton/SingletonPattern.py

class DL:
    class __DataBase:
        def __init__(self):
            pass

        def get_CBS_he_links(self):
            links = []
            try:
                with open(r'../DataBase/heb_pages_links.txt', 'r', encoding="utf-8") as f:
                    for line in f:
                        li = line.split()
                        cbs_link = CbsLink(li[0])
                        cbs_link.name = ' '.join(li[1:])
                        links.append(cbs_link)
                    f.close()
            except Exception as e:
                print(e)
                print('database file did not read', e)
            return links

        def get_CBS_en_links(self):
            links = []
            try:
                with open(r'../DataBase/en_pages_links.txt', 'r', encoding="utf-8") as f:
                    for line in f:
                        li = line.split()
                        cbs_link = CbsLink(li[0])
                        cbs_link.name = ' '.join(li[1:])
                        links.append(cbs_link)
                    f.close()
            except Exception as e:
                print(e)
                print('database file did not read', e)
            return links

        def get_CBS_he_pages(cls):
            links = cls.get_CBS_he_links()  # the links only saved locally
            pages = [SubjectPage(link, link.name) for link in links]
            return pages

        def get_CBS_en_pages(cls):
            links = cls.get_CBS_en_links()
            pages = [SubjectPage(link, link.name) for link in links]
            return pages

        # @classmethod
        # def get_cbs_pages_online(cls):
        #     driver = TestUtility.get_sessions()[0]  # returns a one obj list with defualt driver
        #     driver.get(Links.CBS_MAP_SITE_HE.value) # opens the map site for extracting the links inside
        #     raw_urls = driver.find_elements_by_xpath(Links.MAP_LINKS_XPATH)
        #     print('number of link objects found: ', len(raw_urls))
        #     pages = list(map(lambda x: CbsPage(CbsLink(x.get_attribute('href')), x.text), raw_urls))
        #     driver.close()
        #     return pages

        def save_test_result(cls, test_key, page: SubjectPage):
            try:
                path = r'../TestData/logs'
                file = path + '\\' + test_key + '.html'
                with open(file, 'a', encoding='utf-8') as f:
                    style = 'style={color:red; font-size: large; }'
                    page_link = '<h1 {}><a style="color:red" href="{}" target="_blank" >{}</a></h1><br>'.format(style,
                                                                                                                page.link.url,
                                                                                                                page.name)
                    errors = ('<h1 {}>' + str(page.get_errors()) + '</h1><br>').format(style)
                    f.write(page_link + errors)
                f.close()
            except Exception as e:
                print('exception in db')
                raise e


        def get_test_result(cls, file_key):
            file_name = file_key
            try:
                path = r'../TestData/logs'
                file = path + '\\' + file_name + '.html'
                with open(file, 'r', encoding='utf-8') as f:
                    data = f.read()
                f.close()
                return data, file
            except Exception as e:
                print('exception in db reading file content')
                raise e

        def save_summary_result(cls, file_key, summary):
            sum = '<h1 style="color:black" style={color:red; font-size: large; }>Test started on: ' + str(
                summary[0]) + ' ' + str(summary[1]) + '<br>'
            sum += 'Total pages: ' + str(summary[2]) + '<br>'
            sum += 'Tested: ' + str(summary[3]) + '<br>'
            sum += 'Total error pages: ' + str(summary[4]) + '</h1>'
            file_name = file_key
            try:
                path = r'../TestData/logs'
                file = path + '\\' + file_name + '.html'
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    f.close()
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(sum + '<br>' + content)
                f.close()
            except Exception as e:
                print('exception in db writing summery')
                raise e

        def load_xpath(cls, key):
            with open(r'../Configuration/xpath.json', 'rb') as f:
                data = json.load(f)
                f.close()
            return data['XPath'][0][key]

    class Links(Enum):
        CBS_HOME_PAGE_HE = 'https://www.cbs.gov.il/he/Pages/default.aspx'
        CBS_MAP_SITE_HE = 'https://www.cbs.gov.il/he/pages/sitemap.aspx'
        CBS_MAP_SITE_EN = 'https://www.cbs.gov.il/en/Pages/sitemap.aspx'
        ROOT_DIR = sys.path[1]
        CHROME_DRIVER = ROOT_DIR + "/WebDrivers/92.0.4515.43/chromedriver_win32.exe"
        MAP_LINKS_XPATH = DataBase.load_xpath('MAP_LINKS_XPATH')
        HEBREW_STATS_XPATH = DataBase.load_xpath('HEBREW_STATS_XPATH')
        RIGHT_EXTRA_PARTS_XPATH = DataBase.load_xpath('RIGHT_EXTRA_PARTS_XPATH')
        LEFT_EXTRA_PARTS_XPATH = DataBase.load_xpath('LEFT_EXTRA_PARTS_XPATH')
        TOOLS_AND_DB_XPATH = DataBase.load_xpath('TOOLS_AND_DB_XPATH')
        SUMMARY_XPATH = DataBase.load_xpath('SUMMARY_XPATH')
        TOP_BOX_XPATH = DataBase.load_xpath('TOP_BOX_XPATH')
        SUB_SUBJECTS_XPATH = DataBase.load_xpath('SUB_SUBJECTS_XPATH')
        PRESS_RELEASES_XPATH = DataBase.load_xpath('PRESS_RELEASES_XPATH')
        TABLES_AND_CHARTS_XPATH = DataBase.load_xpath('TABLES_AND_CHARTS_XPATH')
        PUBLICATIONS_XPATH = DataBase.load_xpath('PUBLICATIONS_XPATH')
    #static - belongs to the class
    instance = None
    def __init__(self, arg):
        if not DL.instance:
            DL.instance = DL.__DataBase(arg)
            print('instance was created')
        else:
            DL.instance.val = arg
            print('instance already exist')
    def get_instance(self):
        return OnlyOne.instance
    # def __getattr__(self, name):
    #     return getattr(self.instance, name)

x = OnlyOne('sausage')
print('x: '+ str(x))

y = OnlyOne('eggs')
print('y: '+ str(y))
z = OnlyOne('spam')
print('z: '+ str(z))

print('x: '+ str(x))
print('y: '+ str(y))
# print(x.__getattr__())
# print(repr(y))
# print(repr(z))
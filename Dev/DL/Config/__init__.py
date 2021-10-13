import json
import sys


class Config:
    def __init__(self):
        pass

    @classmethod
    def get_xpath(cls):
        cur_dir = sys.path[1] + '\\Dev\\DL\\Config\\'
        with open(cur_dir + 'xpath.json', 'r',encoding='utf-8') as f:
            data = json.load(f)
            f.close()
            return data

    @classmethod
    def get_driver(cls):
        cur_dir = sys.path[1] + '\\Dev\\DL\\Config\\'
        with open(cur_dir + 'webdriver_path.json', 'r') as f:
            data = json.load(f)
            f.close()
            return data




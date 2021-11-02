import json
import sys


class Config:

    @classmethod
    def get_xpath(cls):
        cur_dir = sys.path[1] + '\\Dev\\DL\\Config\\'
        with open(cur_dir + 'xpath.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            f.close()
            return data

    @classmethod
    def get_driver(cls):
        cur_dir = sys.path[1] + '\\Dev\\DL\\Config\\'
        with open(cur_dir + 'path.json', 'r') as f:
            data = json.load(f)
            f.close()
            return sys.path[1] + '\\Dev\\DL\\WebDrivers' + data['driver_path']




import json

from selenium import webdriver

with open('webdriver_path.json','rb') as file:
    data = json.load(file)
    file.close()
print(data['driver_path'])
driver = webdriver.Chrome("C:\chromedriver.exe")
driver.get('https://chromedriver.chromium.org/')
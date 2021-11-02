import urllib.request

r = urllib.request.urlopen('https://www.cbs.gov.il/he/settlements?subject=%D7%9E%D7%A9%D7%A7%D7%99%20%D7%91%D7%99%D7%AA%gh%gs').read()
with open('decoded.html','wb') as f:
    f.write(r)
    f.close()
# import requests
#
# r = requests.get('https://www.cbs.gov.il/he/settlements?subject=%D7%9E%D7%A9%D7%A7%D7%99%20%D7%91%D7%99%D7%AA%gh%gs')

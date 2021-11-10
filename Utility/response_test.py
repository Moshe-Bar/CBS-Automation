import ssl
import urllib.request
import certifi
import urllib3
CERT_CONTEXT=ssl.create_default_context(cafile=certifi.where())

# print('after imports')
# url = 'https://www.gov.il/he/departments/ministry_of_health/govil-landing-page'
# url = r'D:\Current\cbs_auto\TestData\logs\01_Jun_2021_11.10.39.html'
# r = urllib3.
# with open('decoded.html','wb') as f:
#     f.write(r.read())
#     f.close()
# print(r.getcode())
# import requests
# context=ssl.create_default_context(cafile=certifi.where())
# r = requests.get('https://www.cbs.gov.il/he/settlements?subject=%D7%9E%D7%A9%D7%A7%D7%99%20%D7%91%D7%99%D7%AA%gh%gs')


# print('before ver1 cert')
# r = urllib.request.urlopen(url, context=CERT_CONTEXT)
# status_code = r.getcode()
# print('ver1: ', status_code)
#
# print('before ver1')
# r = urllib.request.urlopen(url)
# print('ver3: ', r.getcode())


print('before ver3')
import urllib3
import certifi
http = urllib3.PoolManager(ca_certs=certifi.where())

url = 'https://httpbin.org/anything'



resp = http.request('GET', url)
status_code = resp.status
data = resp.data.decode('utf-8')

print(status_code)
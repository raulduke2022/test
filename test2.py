# # a = {
# #   "requestTime": "19.03.2023 09:13",
# #   "RequestResult": {
# #     "diagnosticCards": [
# #       {
# #         "dcExpirationDate": "2023-12-14",
# #         "pointAddress": "109651, Москва Город, Москва г., Марьино, Иловайская, дом 3А, строение 7, ",
# #         "chassis": "ОТСУТСТВУЕТ",
# #         "body": "Z94K241BBMR251210",
# #         "operatorName": "11495",
# #         "pdfBase64": null,
# #         "odometerValue": "121032",
# #         "dcNumber": "114951052200660",
# #         "dcDate": "2022-12-14",
# #         "previousDcs": [
# #           {
# #             "odometerValue": "670",
# #             "dcExpirationDate": "2023-02-11",
# #             "dcNumber": "076350112101327",
# #             "dcDate": "2021-02-10"
# #           }
# #         ],
# #         "success": true,
# #         "vin": "Z94K241BBMR251210",
# #         "model": "Solaris",
# #         "brand": "HYUNDAI"
# #       }
# #     ],
# #     "error": null,
# #     "status": "OK"
# #   },
# #   "hostname": "h8-check0-dc",
# #   "vin": "Z94K241BBMR251210",
# #   "status": 200
# # }
# import time
# from requests_html import HTMLSession
# asession = HTMLSession()
#
# def get_pythonorg():
#   r = asession.get('https://python.org/')
#   print(r)
#
# start = time.time()
# print("hello")
# for i in range(50):
#   get_pythonorg()
# end = time.time()
# print(end - start)
#
# #9.17586064338684

from requests_html import HTMLSession

proxies = ['193.124.177.120:9624', '194.67.197.229:9857', '194.67.198.70:9527']
login_pass = {
        'login': 'GKrm9k',
        'pass': 'LeR86P'
    }

def get_proxy(proxy):
    proxies = {'https': 'https://GKrm9k:LeR86P@194.67.197.229:9857'}
    return proxies
    print(proxies)

s = HTMLSession()
proxies = get_proxy(proxies[0])
print(proxies)
link = 'https://requests.readthedocs.io/'
r = s.get(link, proxies=proxies)
print(r)


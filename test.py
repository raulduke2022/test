# a = {
#   "requestTime": "19.03.2023 09:13",
#   "RequestResult": {
#     "diagnosticCards": [
#       {
#         "dcExpirationDate": "2023-12-14",
#         "pointAddress": "109651, Москва Город, Москва г., Марьино, Иловайская, дом 3А, строение 7, ",
#         "chassis": "ОТСУТСТВУЕТ",
#         "body": "Z94K241BBMR251210",
#         "operatorName": "11495",
#         "pdfBase64": null,
#         "odometerValue": "121032",
#         "dcNumber": "114951052200660",
#         "dcDate": "2022-12-14",
#         "previousDcs": [
#           {
#             "odometerValue": "670",
#             "dcExpirationDate": "2023-02-11",
#             "dcNumber": "076350112101327",
#             "dcDate": "2021-02-10"
#           }
#         ],
#         "success": true,
#         "vin": "Z94K241BBMR251210",
#         "model": "Solaris",
#         "brand": "HYUNDAI"
#       }
#     ],
#     "error": null,
#     "status": "OK"
#   },
#   "hostname": "h8-check0-dc",
#   "vin": "Z94K241BBMR251210",
#   "status": 200
# }
import time
from requests_html import AsyncHTMLSession
asession = AsyncHTMLSession()

async def get_pythonorg():
  print('starting')
  r = await asession.get('https://python.org/')
  print(r)

start = time.time()
for i in range(150):
  asession.run(get_pythonorg)

end = time.time()
print(end - start)


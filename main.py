from requests_html import AsyncHTMLSession #requests module
from anticaptchaofficial.imagecaptcha import * #captcha module
import base64 #make image from base64 string
from fake_useragent import UserAgent #generate user-agent
import pandas as p
import time
from peewee import *
from database import Data

#__________PROXIES__________#

proxies = ['193.124.177.120:9624', '194.67.197.229:9857', '194.67.198.70:9527']
login_pass = {
        'login': 'GKrm9k',
        'pass': 'LeR86P'
    }

def get_proxy(proxy_ip, proxy_port):
    proxies = {f"https': 'https://GKrm9k:LeR86P@{proxy_ip}:{proxy_port}"}
    return proxies

#__________DATABASE__________#

db = SqliteDatabase('people.db')
db.connect()


#____________________________________#

URL_CAPTCHA = 'https://check.gibdd.ru/captcha'
RESTRICT_URL = 'https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/auto/restrict'
DIAGNOSTIC_URL = 'https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/auto/diagnostic'

#generating user-agent
ua = UserAgent()
user_agent = ua.chrome

#setting headers
HEADERS = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

df = p.read_excel(io='cars.xlsx')
cars = df.to_dict('records')


async def main():

    for i in range(len(cars)):
        # time.sleep(10)
        vin_nomer = cars[i]['VIN']

        #create session getting captcha information
        proxy = random.choice(free_proxies)

        asession = AsyncHTMLSession()
        url = URL_CAPTCHA
        r = await asession.get(url, proxies={'http': proxy, 'https': proxy})
        token = r.json()['token']
        image = r.json()['base64jpg']

        #creating image
        with open("imageToSave.png", "wb") as fh:
          fh.write(base64.urlsafe_b64decode(image))

        #solving captcha
        solver = imagecaptcha()
        solver.set_verbose(1)
        solver.set_key("b78746e5f1f1678b4050533a1667e4be")
        solver.set_soft_id(0)
        captcha_text = solver.solve_and_return_solution("imageToSave.png")
        if captcha_text != 0:
            result = True
            # print("captcha text "+captcha_text)
        else:
            # print("task finished with error "+solver.error_code)
            solver.report_incorrect_image_captcha()
            result = False

        #sending request to gibdd
        if result:
            print('waiting 10 sec')
            # time.sleep(10)
            data = {
                "vin": vin_nomer,
                "checkType": 'restricted',
                "captchaWord": captcha_text,
                "captchaToken": token
            }
            r = await asession.post(DIAGNOSTIC_URL, headers=HEADERS, data=data, proxies={'http': proxy, 'https': proxy})
            if r.status_code == 200:
                print(r.status_code)
                r = r.json()
                main_info = r.get('RequestResult').get('diagnosticCards')[0]
                print(f'main info {main_info}')
                new_data = Data()
                new_data.requestTime = r.get('requestTime')
                if main_info:
                    new_data.dcExpirationDate = main_info.get('dcExpirationDate')
                    new_data.pointAddress = main_info.get('pointAddress')
                    new_data.chassis = main_info.get('chassis')
                    new_data.operatorName = main_info.get('operatorName')
                    new_data.odometerValue = main_info.get('odometerValue')
                    new_data.dcNumber = main_info.get('dcNumber')
                    new_data.model = main_info.get('model')
                    new_data.brand = main_info.get('brand')
                else:
                    print('didnt get main_info')
                new_data.save()
                print("data added to db")
            else:
                print('solved not correct')
                i -= 1
        else:
            i -= 1
            print('couldnt solve')


db.close()



if __name__ == "__main__":
    main()






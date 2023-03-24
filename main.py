from anticaptchaofficial.imagecaptcha import * #captcha module
import base64 #make image from base64 string
from fake_useragent import UserAgent #generate user-agent
import pandas as p
from peewee import *
from database import Data
import aiohttp
import asyncio
import time
start_time = time.time()


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
FREE_PROXIES = []

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

async def solve_captcha(session, url, vin_nomer):
    async with session.get(url) as resp:
        answer = await resp.json()
        token = answer['token']
        image = answer['base64jpg']

        # creating image
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.urlsafe_b64decode(image))

        # solving captcha
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

        if captcha_text:
            print('waiting 10 sec')
            # time.sleep(10)
            data = {
                "vin": vin_nomer,
                "checkType": 'restricted',
                "captchaWord": captcha_text,
                "captchaToken": token
            }
            print('we are here')
            async with session.post(DIAGNOSTIC_URL, headers=HEADERS, data=data) as resp:
                r = await resp.json()
                print(r)

            if resp.status == 200:
                print(resp.status)
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
        else:
            print('couldnt solve')



async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(len(cars)):
            vin_nomer = cars[i]['VIN']
            url = URL_CAPTCHA

            #create session getting captcha information
            tasks.append(asyncio.ensure_future(solve_captcha(session, url, vin_nomer=vin_nomer)))

        await asyncio.gather(*tasks)


db.close()



if __name__ == "__main__":
    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))







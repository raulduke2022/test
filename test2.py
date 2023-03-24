# proxies = ['193.124.177.120:9624', '194.67.197.229:9857', '194.67.198.70:9527']
# login_pass = {
#         'login': 'GKrm9k',
#         'pass': 'LeR86P'
#     }
#
# link = 'https://requests.readthedocs.io/'

import aiohttp
import asyncio
import time

start_time = time.time()


async def get_pokemon(session, url):
    async with session.get(url) as resp:
        pokemon = await resp.json()
        return pokemon['name']


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = []
        for number in range(1, 5):
            url = f'https://pokeapi.co/api/v2/pokemon/{number}'
            tasks.append(asyncio.ensure_future(get_pokemon(session, url)))

        await asyncio.gather(*tasks)



import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import time
import asyncio

async def finder_cards(search: str = 'Зубная щётка', page: str = '1') -> list:
    
    ua = UserAgent()
    headers = {'User-Agent': ua.random,
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                "Referer": "https://www.wildberries.ru/",
                "Accept": "application/json"}
    data = []
    for i in range(1, int(page)+1):
        url = f'https://u-search.wb.ru/exactmatch/ru/common/v18/search?query={search}&page={i}&resultset=catalog&sort=popular&dest=-1257786'
        try:
            req = requests.get(url=url, headers=headers)
            res = req.json()
            # soup = BeautifulSoup(res, 'lxml')
            index = 0
            with open(f'res{i}.json', 'w', encoding='utf-8') as file:
                json.dump(res, file, indent=4, ensure_ascii=False)

            while True:
                try:
                    data.append({'name': res.get('products')[index].get('name'),
                                'url': f'https://www.wildberries.ru/catalog/{res.get('products')[index].get('id')}/detail.aspx'})

                except:
                    if index >= len(res.get('products')):
                        time.sleep(10)
                        break
                
                index += 1
        except:
            continue
    return data
        
if __name__ == '__main__':
    asyncio.run(finder_cards(search='Зубная щётка', page='2'))


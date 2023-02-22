import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

list_cat_url = []
carts = []
count = 0

start_time = time.time()

url = "https://www.grandline.ru"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
}
url_catalog = "https://www.grandline.ru/katalog"
req = requests.get(url_catalog, headers=headers)
soup = BeautifulSoup(req.text, "lxml")

list_catigories_1lv = soup.find_all('a', class_="category-item__preview")
for item in tqdm(list_catigories_1lv):
    req = requests.get(f"https://www.grandline.ru{item.get('href')}", headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    list_cat_url.append({
        'url_cat': f"{url}{item.get('href')}",
    })

    # Цикл для перехода по разделам
    for item in tqdm(list_cat_url):
        req = requests.get(item['url_cat'])
        soup = BeautifulSoup(req.text, "lxml")

        count += 1
        print(f"Обработка {count} каталога ")

        # найти последнее значение в пагинации
        pages_count = int(soup.find("ul", class_="paging").find_all("a", class_="paging__link")[-2].text)

        # цикл по пагинации
        for i in range(1, 2): # pages_count + 1):
            url_page = f"{item['url_cat']}?page={i}"

            req = requests.get(url_page, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")

            list_item_cart = soup.find_all('div', 'product-item__inner')
            for item_cart in list_item_cart:
                url = ""
                name = ""
                price = ""
                try:
                    url = "https://www.grandline.ru" + item_cart.find('strong', class_="product-item__title").find('a').get('href')
                except Exception:
                    url = 'none'
                try:
                    name = item_cart.find('strong', class_="product-item__title").find('a').getText()
                except Exception:
                    name = 'none'
                try:
                    price = re.search('[0-9. ]+',item_cart.find('strong', class_="product-item__price").getText()) # Вытащить цену
                except Exception:
                    price = 'none'

                carts.append({
                    "url": url,
                    "name": name,
                    "price": price.group(0),
                })
                print(carts)
                exit()
print(carts)
# with open("../resul_parce/carts_grandline.json", "w", encoding="utf-8") as file:
#     json.dump(carts, file, indent=4, ensure_ascii=False)

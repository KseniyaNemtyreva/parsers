# Некоректный вывод цены
import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

start_time = time.time()

list_cat_url = []
count = 0
carts = []

url = "https://stroimaks.ru"

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, "lxml")

list_catigories_url = soup.find_all('div', class_="s-inner")
for item in list_catigories_url:
    item = item.find('a').get('href')
    if item == "/aktsiya/":
        continue
    list_cat_url.append({
        'url_cat': f"{url}{item}",
    })

# Цикл для перехода по разделам
for item in tqdm(list_cat_url):
    req = requests.get(item['url_cat'], headers=headers)
    soup = BeautifulSoup(req.text, "lxml")

    count += 1
    print(f"Обработка {count} каталога ")

    try:
        # найти последнее значение в пагинации
        pages_count = int(soup.find("ul", class_="c-pagination").find_all("a")[-2].text)
        # цикл по пагинации
        for i in range(1, pages_count + 1):
            url_page = f"{item['url_cat']}?page={i}"

            req = requests.get(url_page, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")

            link_products_list = soup.find_all('div', 'thumbnail-catalog one-product')
            for item_cart in link_products_list:
                try:
                    url = "https://stroimaks.ru" + item_cart.find('div', class_="name").find("a").get('href')
                except Exception:
                    url = 'none'
                try:
                    name = item_cart.find('div', class_="name").find("a").getText()
                except Exception:
                    name = 'none'
                try:
                    price = re.search('[0-9 ]+',item_cart.find('div', class_="price").find("span").getText())
                except Exception:
                    price = 'none'

                carts.append({
                    "url": f"{url}",
                    "name": name,
                    "price": price.group(0),
                })
    except Exception:
        url_page = f"{item['url_cat']}"

        req = requests.get(url_page, headers=headers)
        soup = BeautifulSoup(req.text, "lxml")

        link_products_list = soup.find_all('div', 'thumbnail-catalog one-product')
        for item_cart in link_products_list:
            try:
                url = "https://stroimaks.ru" + item_cart.find('div', class_="name").find("a").get('href')
            except Exception:
                url = 'none'
            try:
                name = item_cart.find('div', class_="name").find("a").getText()
            except Exception:
                name = 'none'
            try:
                price = re.search('[0-9 ]+', item_cart.find('div', class_="price").find("span").getText())
            except Exception:
                price = 'none'

            carts.append({
                "url": url,
                "name": name,
                "price": price.group(0),
            })
# print(carts)
with open("../resul_parce/carts_stroimaks.json", "w", encoding="utf-8") as file:
    json.dump(carts, file, indent=4, ensure_ascii=False)

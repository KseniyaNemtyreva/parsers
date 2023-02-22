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

url = "https://vertical.ru"

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
}
url_catalog = "https://vertical.ru/catalog/"
req = requests.get(url_catalog, headers=headers)
soup = BeautifulSoup(req.text, "lxml")

list_catigories_url = soup.find_all('div', class_="col-xl-2")
for item in list_catigories_url:
    item = item.find('a').get('href')
    list_cat_url.append({
        'url_cat': f"{url}{item}",
    })

# Цикл для перехода по разделам
for item in tqdm(list_cat_url):
    req = requests.get(item['url_cat'], headers=headers)
    soup = BeautifulSoup(req.text, "lxml")

    count += 1
    print(f"Обработка {count} каталога ")

    # найти последнее значение в пагинации
    pages_count = int(soup.find("ul", class_="pagination").find_all("a")[-2].text)
    # цикл по пагинации
    for i in range(1, pages_count + 1):
        url_page = f"{item['url_cat']}?PAGEN_1={i}"

        req = requests.get(url_page, headers=headers)
        soup = BeautifulSoup(req.text, "lxml")

        link_products_list = soup.find_all('div', 'catalog-item js-catalog-item')
        for item_cart in link_products_list:
            url = ""
            name = ""
            price = ""
            try:
                url = "https://vertical.ru" + item_cart.find('a', class_="catalog-item-link js-catalog-item-link").get('href')
            except Exception:
                url = 'none'
            try:
                name = item_cart.find('div', class_="item-info-name").find("a").getText()
            except Exception:
                name = 'none'
            try:
                price = re.search('[0-9]+',item_cart.find('div', class_="item-info-price-value").getText())
            except Exception:
                price = 'none'

            carts.append({
                "url": url,
                "name": name,
                "price": price.group(0),
            })
# print(carts)
with open("../resul_parce/carts_vertical.json", "w", encoding="utf-8") as file:
    json.dump(carts, file, indent=4, ensure_ascii=False)

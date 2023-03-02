import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

start_time = time.time()

list_cat_url = []
list_cat_2url = []
count = 0
carts = []

url = "https://www.maxidom.ru"
headers = {
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
}
url_catalog = f"{url}/catalog"
req = requests.get(url_catalog, headers=headers)
soup = BeautifulSoup(req.text, "lxml")

list_catigories_1lv = soup.find_all('a', class_="it_categories_a")
for item in list_catigories_1lv:
    item = item.get('href')
    list_cat_url.append({
        'url_cat': f"{url}{item}",
    })

# Цикл для перехода по разделам
for item in tqdm(list_cat_url):
    req = requests.get(item['url_cat'], headers=headers)
    soup = BeautifulSoup(req.text, "lxml")

    count += 1
    print(f"Сборка ссылок с {count} каталога ")

    list_catigories_2lv = soup.find_all(class_="it_categories_a")
    for item in list_catigories_2lv:
        if item.get("href"):
            item = item.get("href")

            list_cat_2url.append({
                'url_cat': f"{url}{item}",
            })
        else:
            item = item.find_all("a")
            item = item[1].get("href")
            list_cat_2url.append({
                'url_cat': f"{url}{item}",
            })

# Цикл для перехода по категориям
for item in tqdm(list_cat_2url):
    req = requests.get(item['url_cat'], headers=headers)
    soup = BeautifulSoup(req.text, "lxml")

    try:
        # найти последнее значение в пагинации
        pages_count = int(soup.find("ul", class_="ul-cat-pager").find_all("a")[-2].text)
        # цикл по пагинации
        for i in range(1, 2): # pages_count + 1):
            url_page = f"{item['url_cat']}?PAGEN_3={i}"

            req = requests.get(url_page, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")

            link_products_list = soup.find_all('article', 'item-list group')
            for item_cart in link_products_list:
                try:
                    url = "https://grmsd.ru" + item_cart.find('a', class_="name-big").get('href')
                except Exception:
                    url = 'none'
                try:
                    name = item_cart.find('a', class_="name-big").getText()
                except Exception:
                    name = 'none'
                try:
                    price = re.search('[0-9 ]+', item_cart.find('span', class_="price-list").getText().strip())
                except Exception:
                    price = 'none'

                carts.append({
                    "url": url,
                    "name": name.strip(),
                    "price": price.group(0),
                })
                # print(carts)
    except:
        link_products_list = soup.find_all('article', 'item-list group')
        for item_cart in link_products_list:
            try:
                url = "https://grmsd.ru" + item_cart.find('a', class_="name-big").get('href')
            except Exception:
                url = 'none'
            try:
                name = item_cart.find('a', class_="name-big").getText()
            except Exception:
                name = 'none'
            try:
                price = re.search('[0-9 ]+', item_cart.find('span', class_="price-list").getText().strip())
            except Exception:
                price = 'none'

            carts.append({
                "url": url,
                "name": name.strip(),
                "price": price.group(0),
            })
            # print(carts)
# print(carts)
with open("../resul_parce/carts_maxidom.json", "w", encoding="utf-8") as file:
    json.dump(carts, file, indent=4, ensure_ascii=False)
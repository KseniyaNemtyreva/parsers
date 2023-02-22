import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

start_time = time.time()

list_cat_url = []
count = 0
carts = []

url = "https://grmsd.ru/catalog/"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, "lxml")

list_catigories_1lv = soup.find_all('div', class_="item_block")
for item in list_catigories_1lv:
    item = item.find('a').get('href')
    list_cat_url.append({
        'url_cat': f"https://grmsd.ru{item}",
    })

# Цикл для перехода по разделам
for item in tqdm(list_cat_url):
    req = requests.get(item['url_cat'], headers=headers)
    soup = BeautifulSoup(req.text, "lxml")

    count += 1
    print(f"Обработка {count} каталога ")

    # найти последнее значение в пагинации
    pages_count = int(soup.find("div", class_="nums").find_all("a")[-1].text)
    # цикл по пагинации
    for i in range(1, pages_count + 1):
        url_page = f"{item['url_cat']}?PAGEN_1={i}"

        req = requests.get(url_page, headers=headers)
        soup = BeautifulSoup(req.text, "lxml")

        link_products_list = soup.find_all('div', 'item_block')
        for item_cart in link_products_list:
            try:
                url = "https://grmsd.ru" + item_cart.find('a', class_="font_sm").get('href')
            except Exception:
                url = 'none'
            try:
                name = item_cart.find('a', class_="font_sm").find("span").getText()
            except Exception:
                name = 'none'
            try:
                price = item_cart.find('span', class_="price_value").getText()
            except Exception:
                price = 'none' # Цены нет, если нет в наличие

            carts.append({
                "url": f"{url}",
                "name": name,
                "price": price,
            })
# print(carts)
with open("../resul_parce/carts_grmsd.json", "w", encoding="utf-8") as file:
    json.dump(carts, file, indent=4, ensure_ascii=False)

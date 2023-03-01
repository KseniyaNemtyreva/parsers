import requests
import json
import time
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

start_time = time.time()

list_cat_url = []
count = 0
carts = []

url = "https://vsksnab.ru/shop/"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, "lxml")

# найти последнее значение в пагинации
pages_count = int(soup.find("ul", class_="page-numbers").find_all("a", class_="page-numbers")[-2].text)
# цикл по пагинации
for i in tqdm(range(1, pages_count + 1)):
    if i == 1:
        url_page = url
    else:
        url_page = f"{url}page/{i}/"
    

    req = requests.get(url_page, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")

    link_products_list = soup.find_all('li', 'type-product')

    for item_cart in link_products_list:
        try:
            urli = item_cart.find('a', class_="woocommerce-LoopProduct-link").get('href')
        except Exception:
            url = 'none'
        try:
            name = item_cart.find('h2', class_="woocommerce-loop-product__title").getText()
        except Exception:
            name = 'none'
        try:
            price = re.search('[0-9,]+',
                              item_cart.find('span', class_="woocommerce-Price-amount amount").find('bdi').getText())
        except Exception:
            price = 'none'

        carts.append({
            "url": urli,
            "name": name,
            "price": price.group(0),
        })


# print(carts)


with open("resul_parce/carts_vsksnab.json", "w", encoding="utf-8") as file:
    json.dump(carts, file, indent=4, ensure_ascii=False)

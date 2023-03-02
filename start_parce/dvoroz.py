# Нужна функция
# Во втором каталоге есть 5 уровень, а также имеются карточки с другой структурой строения
import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import re


carts = []

list_cat_url = []
count = 0

url = "http://dvoroz.ru/sitemap_tovar.xml"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.3.949 Yowser/2.5 Safari/537.36"
}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, "xml")

list_catigories_url = soup.find_all('loc')
for item in list_catigories_url:
    item = item.getText()
    list_cat_url.append(item)


# Цикл для перехода по карточкам
for item in tqdm(list_cat_url):
    req = requests.get(item, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")

    count += 1
    print(f"Обработка {count} карточки")

    try:
        url = item
    except Exception:
        url = 'none'
    try:
        name = soup.find('h1', class_="text-center").getText()
    except Exception:
        name = 'none'
    try:
        print()
        # price = re.search('[0-9.]+', soup.find('div', class_="treeview").getText())
    except Exception:
        price = 'none'

    carts.append({
        "url": url,
        "name": name,
        # "price": price.group(0),
    })
    print(carts)
    exit()
# print(carts)


    # with open("../resul_parce/carts_discont.json", "w") as file:
    #     json.dump(carts, file, indent=4, ensure_ascii=False)



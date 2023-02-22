import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

start_time = time.time()

list_cat_url = []
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
    print(f"Обработка {count} каталога ")

    list_catigories_2lv = soup.find_all('figure', class_="category-first")
    for item in list_catigories_2lv:
        item = item.find("a").find_next().get('href')
        print(item)
        exit()
        list_cat_url.append({
            'url_cat': f"{url}{item}",
        })

import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

start_time = time.time()

list_cat_url = []
count = 0
carts = []

url = "https://famarket.ru/"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, "lxml")

list_catigories_1lv = soup.find_all('ul', class_="list-group left-menu")
for item in list_catigories_1lv:
    item = item.find('a', class_="sub-marker").get('href')
    list_cat_url.append({
        'url_cat': f"https://famarket.ru{item}",
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
        url_page = f"{item['url_cat']}" # ??
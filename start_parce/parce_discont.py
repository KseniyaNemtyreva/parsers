import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

start_time = time.time()

carts = []

url = "https://xn--d1aiddpfbpfdkb.xn--p1ai/katalog"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}

req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, "lxml")

with open("html_startPage/discont.html", "w") as file:
    file.write(req.text)

list_catigories_1lv = soup.find_all('a', class_="popular_item")
for item in tqdm(list_catigories_1lv):
    req = requests.get(f"https://xn--d1aiddpfbpfdkb.xn--p1ai{item.get('href')}", headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    
    list_catigories_2lv = soup.find_all('a', class_="popular_item")
    for item_page in list_catigories_2lv:
        req = requests.get(f"https://xn--d1aiddpfbpfdkb.xn--p1ai{item_page.get('href')}", headers=headers)
        soup = BeautifulSoup(req.text, "lxml")

        list_item_cart = soup.find_all('div', class_="main_goods_item")
        #print(list_item_cart)
        for item_cart in list_item_cart:
            try:
                url = item_cart.find('a', class_="goods_title").get('href')
            except Exception:
                url = 'none'
            try:
                name = item_cart.find('a', class_="goods_title").getText()
            except Exception:
                name = 'none'
            try:
                price = item_cart.find('div', class_="goods_price").getText()
            except Exception:
                price = 'none'

            carts.append({
                "url": f"https://xn--d1aiddpfbpfdkb.xn--p1ai{url}",
                "name": name,
                "price": price.replace('\n', '')
            })
            #print(carts)
    #     print(f"Обрабатываю раздел 2-ого уровня {item_page.get('href')}")
    # print(f"Обрабатываю раздел 1-ого уровня {item.get('href')}")

#print(carts)
with open("resul_parce/carts_discont.json", "w") as file:
    json.dump(carts, file, indent=4, ensure_ascii=False)

print("--- %s seconds ---" % (time.time() - start_time))
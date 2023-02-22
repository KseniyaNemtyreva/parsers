import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

start_time = time.time()
url = "https://stroyoz.ru/catalog"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}

req = requests.get(url, headers=headers)
# src = req.text
carts_arr = []

with open("html_startPage/index_cat.html", 'w') as file:
    file.write(req.text)

with open("html_startPage/index_cat.html") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")

all_catigories_1lvl = soup.find_all('li', class_="name text-center")
all_catigories_1lvl_list = []

for item in all_catigories_1lvl:
    tes = item.find('a', class_="dark_link").get('href')
    all_catigories_1lvl_list.append(tes)
print(f"#Собрал URL с {all_catigories_1lvl_list.__len__()} разделов#")

i = 0
for item in tqdm(all_catigories_1lvl_list):
    
    req = requests.get(f"https://stroyoz.ru{item}", headers=headers).text
    soup = BeautifulSoup(req, "lxml")

    if soup.find('div', class_="nums"):
        block_pagen = soup.find('div', class_="nums").find_all('a', class_="dark_link")
        for last_pagen in block_pagen:pass
        last_pagen = last_pagen.getText()
    else:
        last_pagen = 1

    pagen_index = 1
    for index_pagen in tqdm(range(int(last_pagen))):
        req_pagen = requests.get(f"https://stroyoz.ru{item}/?PAGEN_1={pagen_index}", headers=headers).text
        soup = BeautifulSoup(req_pagen, "lxml")

        carts = soup.find_all('div', class_="catalog_item_wrapp")
        for item_cart in carts:
            if item_cart.find('div', class_="item-title").find('a'):
                url_cart = item_cart.find('div', class_="item-title").find('a').get('href')
            else:
                url_cart = 'none'

            if item_cart.find('div', class_="item-title").find('span'):
                name = item_cart.find('div', class_="item-title").find('span').getText()
            else:
                name = 'none'

            if item_cart.find('span', class_="price_value"):
                price = item_cart.find('span', class_="price_value").getText()
            else:
                price = 'none'

            cart = {
                "url": f"https://stroyoz.ru/{url_cart}",
                "name": name,
                "price": price,
            }

            carts_arr.append(cart)
        #print(f"Обработал страницу {pagen_index} Раздела {item}")

        pagen_index += 1

    i += 1
#print(carts_arr)
with open("resul_parce/carts_stroyoz.json", "w") as file:
    json.dump(carts_arr, file, indent=4, ensure_ascii=False)
#print(all_catigories_1lvl_list)
print("--- %s seconds ---" % (time.time() - start_time))
import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

list_cat_url = []

carts = []
count = 0

start_time = time.time()

url = "https://msk.saturn.net"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.934 Yowser/2.5 Safari/537.36",
}

# Сайт на VUE поэтому request не работает, эмулируем работу браузера через selenium
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(f"{url}/catalog")

try:
    # Преобразовать в soup объект для поиска
    soup = BeautifulSoup(browser.page_source, "lxml")

    link_catigories_list = soup.find_all('li', '_category_nav-item')
    # Получить ссылки на разделы
    for item in link_catigories_list:
        item = item.find('a').get('href')
        list_cat_url.append({
            'url_cat': f"{url}{item}",
        })

    # Цикл для перехода по разделам
    for item in tqdm(list_cat_url):
        browser.get(item['url_cat'])
        soup = BeautifulSoup(browser.page_source, "lxml")

        count += 1
        print(f"Обработка {count} каталога ")

        # найти последнее значение в пагинации
        pages_count = int(soup.find("ul", class_="pagination").find_all("a")[-2].text)

        # цикл по пагинации
        for i in range(1, pages_count + 1):
            url_page = f"{item['url_cat']}?page={i}"
            browser.get(url_page)

            soup = BeautifulSoup(browser.page_source, "lxml")

            link_products_list = soup.find_all('div', 'goods-card')

            for item_cart in link_products_list:
                try:
                    url = "https://msk.saturn.net" + item_cart.find('a', class_="goods-photo").get('href')
                except Exception:
                    url = 'none'
                try:
                    name = item_cart.find('div', class_="goods-name").find("a", class_="g").getText()
                except Exception:
                    name = 'none'
                try:
                    price = item_cart.find('div', class_="block-price").find('div', class_="block-price-value").getText()
                except Exception:
                    price = 'none'

                carts.append({
                    "url": f"{url}",
                    "name": name,
                    "price": price.replace('\n', '').replace('Ä', '').replace('\t', ' ').replace(' ', ''),
                })
    browser.back()
    print(carts)

    with open("../resul_parce/carts_msk_saturn(test).json", "w", encoding="utf-8") as file:
        json.dump(carts, file, indent=4, ensure_ascii=False)

except Exception as _ex:
    print(_ex)
finally:
    browser.quit()

print("--- %s seconds ---" % (time.time() - start_time))

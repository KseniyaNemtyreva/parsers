import requests
import json
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

list_cat_url = []
carts = []

start_time = time.time()

url = "https://xn--80adsfsdepifdc.xn--p1ai"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}
#Сайт на VUE поэтому request не работает, эмулируем работу браузера через selenium
browser = webdriver.Chrome()
browser.get(url)
#Записать страницу в файл(тест)
with open('html_startPage/otvin.html', 'w') as file:
    file.write(browser.page_source)
#Преобразовать в soup объект для поиска
soup = BeautifulSoup(browser.page_source, "lxml")

soup = soup.find('div', class_="row-category")
link_catigories_list = soup.find_all('div','main-catalog-item-head')
#Получить ссылки на разделы
for item in link_catigories_list:
    item = item.find('a').get('href')
    list_cat_url.append({
        'url_cat': f"{url}{item}",
    })

#Цикл для перехода по разделам
for item in tqdm(list_cat_url):
    browser.get(item['url_cat'])
    soup = BeautifulSoup(browser.page_source, "lxml")
    try:
        last_page = soup.find('div', class_="pagination-block").find('a', class_="end-page").get('href').split('=')[1]
    except Exception:
        last_page = 1
    i = 1
    for pagen in tqdm(range(int(last_page))):
        browser.get(f"{item['url_cat']}/?page={i}")
        soup = BeautifulSoup(browser.page_source, "lxml")

        list_carts = soup.find_all('div', class_="product-item")
        for cart_item in list_carts:
            try:
                url_item = cart_item.find('div', class_="desc").find('a').get('href')
            except Exception:
                url_item = 'none'
            try:
                name_item = cart_item.find('div', class_="desc").find('h3').getText()
            except Exception:
                name_item = 'none'
            try:
                price_item = cart_item.find('div', class_="price-value").find('span', class_="current-price").getText()
            except:
                price_item = 'none'

            carts.append({
                'url': f"{url}{url_item}",
                'name': name_item,
                'price': price_item.replace('\n', '').replace(' ', ''),
            })
        #print(f"Обрабатываю раздел {item['url_cat']}\n страница {i}")
        i += 1

with open("resul_parce/carts_otvinta.json", "w") as file:
    json.dump(carts, file, indent=4, ensure_ascii=False)





#print(list_cat_url)





print("--- %s seconds ---" % (time.time() - start_time))
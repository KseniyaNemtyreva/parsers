# Нужна функция
# Во втором каталоге есть 5 уровень, а также имеются карточки с другой структурой строения
import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import re


def list_catigories_lv(soup):
    list_catigories_lv = soup.find_all('a', class_="aname")
    for item_page in list_catigories_lv:
        req = requests.get(f"http://dvoroz.ru{item_page.get('href')}", headers=headers)
        soup = BeautifulSoup(req.text, "lxml")


start_time = time.time()

carts = []

url = "http://dvoroz.ru/dvoroz/inetshop/shop"
headers = {
    "accept": "*/*",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.934 Yowser/2.5 Safari/537.36",
}
count = 0
req = requests.get(url, headers=headers)

soup = BeautifulSoup(req.text, "lxml")
while True:
    if soup.find('ul', class_="ulproducts"):
        list_item_cart = soup.find('ul', class_="ulproducts").find_all('li')
        for item_cart in list_item_cart:
            try:
                url = item_cart.find('a', class_="aname").get('href')
            except Exception:
                url = 'none'
            try:
                name = item_cart.find('a', class_="aname").getText()
            except Exception:
                name = 'none'
            try:
                price = re.search('[0-9.]+', item_cart.find('div', class_='dcontrols').find(
                    'div', class_='dbuttons').find('div', class_='dprice').find('span', class_="sprice").getText())
            except Exception:
                price = 'none'
            carts.append({
                "url": f"http://dvoroz.ru{url}",
                "name": name,
                "price": price.group(0)
            })
            break
    else:
        print("Условие не выполняется")
        list_catigories_lv(soup)


    # list_catigories_1lv = soup.find_all('a', class_="aname")
    # for item in tqdm(list_catigories_1lv):
    #     req = requests.get(f"http://dvoroz.ru{item.get('href')}", headers=headers)
    #     soup = BeautifulSoup(req.text, "lxml")
    #
    #     list_catigories_2lv = soup.find_all('a', class_="aname")
    #     for item_page in list_catigories_2lv:
    #         req = requests.get(f"http://dvoroz.ru{item_page.get('href')}", headers=headers)
    #         soup = BeautifulSoup(req.text, "lxml")
    #         try:
    #             list_catigories_3lv = soup.find_all('a', class_="aname")
    #             for item_page in list_catigories_3lv:
    #                 req = requests.get(f"http://dvoroz.ru{item_page.get('href')}", headers=headers)
    #                 soup = BeautifulSoup(req.text, "lxml")
    #
    #                 if soup.find('ul', class_="ulproducts"):
    #                     list_item_cart = soup.find('ul', class_="ulproducts").find_all('li')
    #                     for item_cart in list_item_cart:
    #                         try:
    #                             url = item_cart.find('a', class_="aname").get('href')
    #                         except Exception:
    #                             url = 'none'
    #                         try:
    #                             name = item_cart.find('a', class_="aname").getText()
    #                         except Exception:
    #                             name = 'none'
    #                         try:
    #                             price = re.search('[0-9.]+', item_cart.find('div', class_='dcontrols').find('div', class_='dbuttons').find('div', class_='dprice').find('span', class_="sprice").getText())
    #                         except Exception:
    #                             price = 'none'
    #                         carts.append({
    #                             "url": f"http://dvoroz.ru{url}",
    #                             "name": name,
    #                             "price": price.group(0)
    #                         })
    #                 elif soup.find('ul', class_="ulcats"):
    #                     list_catigories_4lv = soup.find_all('a', class_="aname")
    #                     for item_page in list_catigories_4lv:
    #                         req = requests.get(f"http://dvoroz.ru{item_page.get('href')}", headers=headers)
    #                         soup = BeautifulSoup(req.text, "lxml")
    #
    #                         list_item_cart = soup.find('ul', class_="ulproducts").find_all('li')
    #                         for item_cart in list_item_cart:
    #                             try:
    #                                 url = item_cart.find('a', class_="aname").get('href')
    #                             except Exception:
    #                                 url = 'none'
    #                             try:
    #                                 name = item_cart.find('a', class_="aname").getText()
    #                             except Exception:
    #                                 name = 'none'
    #                             try:
    #                                 price = re.search('[0-9.]+', item_cart.find('div', class_='dcontrols').find('div',
    #                                                                                                             class_='dbuttons').find(
    #                                     'div', class_='dprice').find('span', class_="sprice").getText())
    #                             except Exception:
    #                                 price = 'none'
    #                             carts.append({
    #                                 "url": f"http://dvoroz.ru{url}",
    #                                 "name": name,
    #                                 "price": price.group(0)
    #                             })
    #                 else:
    #                     continue
    #         except Exception as ex:
    #             print(ex)
    #
    # count += 1
    # print(f"{count} страница")
print(carts)


    # with open("../resul_parce/carts_discont.json", "w") as file:
    #     json.dump(carts, file, indent=4, ensure_ascii=False)
    #
    # print("--- %s seconds ---" % (time.time() - start_time))



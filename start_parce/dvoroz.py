# Нужна функция
# Во втором каталоге есть 5 уровень, а также имеются карточки с другой структурой строения
import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import re


carts = []
count = 0

url = "http://dvoroz.ru/sitemap_tovar.xml"
headers = {
    "accept": "*/*",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.934 Yowser/2.5 Safari/537.36",
}

req = requests.get(url, headers=headers)

soup = BeautifulSoup(req.text, "xml")


print(carts)


    # with open("../resul_parce/carts_discont.json", "w") as file:
    #     json.dump(carts, file, indent=4, ensure_ascii=False)



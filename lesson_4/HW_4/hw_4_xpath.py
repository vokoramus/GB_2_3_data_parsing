'''
1. Написать приложение, которое собирает основные новости с сайтов
    https://lenta.ru,
    https://news.mail.ru,
    https://yandex.ru/news.
Для парсинга использовать XPath. Структура данных должна содержать:
     название источника;
     наименование новости;
     ссылку на новость;
     дата публикации.

2. Сложить собранные данные в БД
'''

from pprint import pprint
import requests
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


url = 'https://lenta.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)


fishing_items = dom.xpath("//div[contains(@class,'topnews')][1]//a[contains(@class,'card-big')]")

fishing_list = []

def fishing_list_append(fishing_items, have_header=False):
    for item in fishing_items:
        fish = {}
        source = "lenta.ru"
        link = item.xpath("@href")[0]
        time = item.xpath(".//time/text()")[0]
        fish['source'] = source
        fish['link'] = link
        fish['time'] = time

        if have_header:
            header = item.xpath(".//h3/text()")[0]
            fish['header'] = header

        # # если нужна нормализация структуры БД:
        # else:
        #     fish['header'] = '---'

        fishing_list.append(fish)


fishing_list_append(fishing_items, have_header=True)

fishing_items = dom.xpath("//div[contains(@class,'topnews')][1]//a[contains(@class,'card-mini')]")
fishing_list_append(fishing_items, have_header=False)


pprint(fishing_list)

# Запись в БД
client = MongoClient('localhost', 27017)
db = client['news_db']              # database
news = db.news                      # collection


for fish in fishing_list:
    try:
        news.insert_one(fish)
    except dke:
        pass

# print(len(news))

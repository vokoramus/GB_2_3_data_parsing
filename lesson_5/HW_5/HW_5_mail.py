'''
Вариант I
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах
в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172#

Вариант II
2) Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.
Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# s = Service('./chromedriver')
# chrome_options = Options()
# chrome_options.add_argument("--headless")

#
driver = webdriver.Chrome(service=s, options=chrome_options,
                          # executable_path='C:/chromedriver/chromedriver.exe'
                          )
# driver.implicitly_wait(10)

driver.get('https://5ka.ru/special_offers')

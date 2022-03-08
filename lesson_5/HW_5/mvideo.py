'''Вариант II
2) Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.
Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pprint import pprint
import re
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


s = Service('./chromedriver')
chrome_options = Options()
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(
    # service=s,
    options=chrome_options,
)

driver.implicitly_wait(10)

driver.get('https://www.mvideo.ru/')

# Прокрутка вниз до раздела "Новинки/в тренде"
my_block = driver.find_element(By.TAG_NAME, 'mvid-shelf-group')
actions = ActionChains(driver)
actions.move_to_element(my_block)
actions.perform()
sleep(3)

# Кнопка "В тренде" - нажатие
button = driver.find_element(By.XPATH, '//mvid-shelf-group//button[2]')
button.click()



# Кнопка "Вперед"
# elem = driver.find_element(By.TAG_NAME, 'body')
# for _ in range(2):
#     elem.send_keys(Keys.ARROW_DOWN)  # прокрутка списка
#
# button = driver.find_element(By.XPATH, "//mvid-carousel[@_ngcontent-serverapp-c248]//button[contains(@class, 'btn forward')]")
# button.click()
# sleep(2)
# button.click()
# sleep(2)

# ===================
# //mvid-shelf-group
# //mvid-product-cards-group[@_ngcontent-serverapp-c248]

xpath_name = "//mvid-product-cards-group[@_ngcontent-serverapp-c248]//div[contains(@class, 'product-mini-card__name')]//a/div"  # .text
xpath_href = "//mvid-product-cards-group[@_ngcontent-serverapp-c248]//div[contains(@class, 'product-mini-card__name')]//a"  # @href
xpath_feedback = "//mvid-product-cards-group[@_ngcontent-serverapp-c248]//div[contains(@class, 'product-mini-card__rating')]//span[contains(@class, 'product-rating__feedback')]"  # .text
xpath_stars = "//mvid-product-cards-group[@_ngcontent-serverapp-c248]//div[contains(@class, 'product-mini-card__rating')]//span[contains(@class, 'value')]"  # .text
xpath_price = "//mvid-product-cards-group[@_ngcontent-serverapp-c248]//span[@class='price__main-value']"  # .text

names = driver.find_elements(By.XPATH, xpath_name)
hrefs = driver.find_elements(By.XPATH, xpath_href)
feedbacks = driver.find_elements(By.XPATH, xpath_feedback)
stars = driver.find_elements(By.XPATH, xpath_stars)
prices = driver.find_elements(By.XPATH, xpath_price)


goods_container = []
for i in range(len(names)):
    d = {}
    d['name'] = names[i].text
    d['href'] = hrefs[i].get_attribute('href')
    d['feedback'] = feedbacks[i].text
    d['star'] = stars[i].text
    d['price'] = prices[i].text

    goods_container.append(d)

pprint(goods_container)

print()
driver.quit()

# Запись в БД
client = MongoClient('localhost', 27017)
db = client['mvideo_goods_db']          # database
mvideo_goods = db.mvideo_goods                      # collection


for good in goods_container:
    try:
        mvideo_goods.insert_one(good)
    except dke:
        pass
'''
Вариант I
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах
в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172#
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

import re


s = Service('./chromedriver')
chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(
    # service=s,
    options=chrome_options,
)

driver.implicitly_wait(10)

driver.get('https://account.mail.ru/')

# =========  АВТОРИЗАЦИЯ  ====================
# ожидаем появления поля ввода логина
wait = WebDriverWait(driver, 10)
el = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'input-0-2-77')))
# except:
#     driver.quit()

elem = driver.find_element(By.CLASS_NAME, 'input-0-2-77')
elem.send_keys('study.ai_172@mail.ru')
elem.send_keys(Keys.ENTER)

# ожидаем появления поля ввода пароля
wait = WebDriverWait(driver, 10)
elem = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))
sleep(1)  # т.к. поле ввода пароля доступно не сразу

# вводим пароль
elem = driver.find_element(By.XPATH, '//input[@type="password"]')
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)

# ожидаем загрузки списка писем
sleep(5)  # TODO:

links_storage = set()
href_storage = set()
links_storage_previous_len = -1

# =========  собираем ссылки на письма  ====================
while len(links_storage) > links_storage_previous_len:  # пока не перестанут прибавляться новые
    links = driver.find_elements(By.CLASS_NAME, "js-message-link")  # либо "messageline__link"
    # links = driver.find_elements(By.CLASS_NAME, "")
    links_storage_previous_len = len(links_storage)
    links_storage = links_storage | set(links)  # пополняем set

    # вытащим ссылки
    n = 1
    for link in links_storage:
        try:
            href = link.get_attribute('href')
            print('===', n, href)
            href_storage.add(href)
            # href_storage = href_storage | set(href)  # пополняем set

            n += 1
        except:
            continue

    print('len(href_storage) = ', len(href_storage))


    elem = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(4):
        elem.send_keys(Keys.PAGE_DOWN)  # прокрутка списка

    print(links_storage_previous_len, len(links_storage))
    print()
    sleep(2)




print('len(links_storage) =============', len(links_storage))

bd = []  # сложим сюда словари с данными из писем

n = 1
for href in href_storage:
    message = {}

    # открыть в новом окне
    driver.execute_script('''window.open("about:blank");''')
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    driver.get(href)  # перешли на страницу письма

    # wait = WebDriverWait(driver, 10)
    # el = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__body')))
    sleep(1)

    # извлекаем id письма из ссылки
    p = re.compile(r'readmsg\/(\d+)')
    m = p.search(href)
    id_ = m.group(1)
    print(id_)
    message['_id'] = id_

    sender = driver.find_element(By.XPATH, "//span[@class='letter__field__contact']")
    date = driver.find_element(By.XPATH, "//span[@class='letter__field__read-created']")
    subject = driver.find_element(By.XPATH, "//div[@class='letter__field__subject']")
    text = driver.find_element(By.XPATH, "//div[@class='letter__body']")

    # sender = driver.find_element(By.CLASS_NAME, "letter__field__contact")
    # date = driver.find_element(By.CLASS_NAME, "letter__field__read-created")
    # subject = driver.find_element(By.CLASS_NAME, "letter__field__subject")
    # text = driver.find_element(By.CLASS_NAME, "letter__body")

    message['sender'] = sender.text
    message['date'] = date.text
    message['subject'] = subject.text
    message['text'] = text.get_attribute('innerHTML')  # собираю html, т.к. многие письма не содержат текст в чистом виде

    bd.append(message)
    driver.close()  # закрыли окно
    driver.switch_to.window(driver.window_handles[0])
    n += 1

    # для ограничения работы скрипта в целях сокращения времени
    MESSAGES_TEST_NUMBER = 10
    if len(bd) > MESSAGES_TEST_NUMBER:
        break

for i, message in enumerate(bd):
    print(f'======== {i} ============')
    for k, v in message.items():
        if k != 'text':
            print(k, ': ', v)
    print('-' * 50)

print(len(bd))

driver.quit()


# Запись в БД
client = MongoClient('localhost', 27017)
db = client['mailru_letters_db']          # database
letters = db.letters                      # collection


for letter in bd:
    try:
        letters.insert_one(letter)
    except dke:
        pass

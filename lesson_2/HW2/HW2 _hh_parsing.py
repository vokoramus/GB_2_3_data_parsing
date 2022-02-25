'''
# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов Superjob и HH.
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#     - Наименование вакансии.
#     - Предлагаемую зарплату (отдельно минимальную и максимальную).
#     - Ссылку на саму вакансию.
#     - Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.

# Можно выполнить по желанию один любой вариант или оба при желании и возможности.
'''

from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json


def vacancies_find(tag):
    data_qa_list = ['vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus',
                    'vacancy-serp__vacancy vacancy-serp__vacancy_standard',
                    ]
    try:
        if tag.get('data-qa') in data_qa_list:
            return True
    except KeyError:
        return False
    return False

def vacancy_parsing(vacancies, vac):
    vacancy_dict = {}

    vacancy_dict['vacancy_name'] = vacancies[vac].a.getText()  # - Наименование вакансии.
    salary_tag = vacancies[vac].find(attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
    vacancy_dict['salary'] = salary_parse(salary_tag) if salary_tag else '---'
    vacancy_dict['vacancy_link'] = vacancies[vac].a['href'].split('?')[0]  # - Ссылку на саму вакансию.
    vacancy_dict['vacancy_source'] = base_url[0]  # - Сайт, откуда собрана вакансия.
    vacancy_dict['vacancy_address'] = vacancies[vac].find(attrs={'data-qa': 'vacancy-serp__vacancy-address'}).getText()
    vacancy_dict['company'] = vacancies[vac].find(attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).getText()
    # data-qa="vacancy-serp__vacancy-employer

    return vacancy_dict

def get_response(url, headers):
    # response = requests.get(url, headers=headers)
    # dom = BeautifulSoup(response.text, 'html.parser')

    browser.get(url)
    dom = BeautifulSoup(browser.page_source, 'html.parser')

    # собираем список вакансий на странице
    # vacancies = dom.find_all(attrs={'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_standard_plus'})
    # vacancies = dom.find_all(attrs={'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_standard'})

    return dom

    # for k, v in vacancies2.items:
    #     vacancies[k] = v

def salary_parse(tag):
    #
    # удалить пробелы
    # ищем "-"
    #     цифры до "-": ДО
    #     цифры после "-": ПОСЛЕ
    #         остальное - валюта
    # если нет "-":
    #     ищем цифры, все что после - валюта
    #     ищем "от" или "до" и помещаем цифру в соотв.поле

    s = tag.getText().replace('\u202f', ' ')
    s = s.replace(' ', '')

    salary_dict = {}
    if '–' in s:
        try:
            salary_dict['min'] = s.split('–')[0]
            rest = s.split('–')[1]

            # отделяем валюту от максимума
            mask = r'\d+'
            reg = re.search(mask, rest)
            salary_dict['max'] = reg[0]
            salary_dict['currency'] = re.sub(mask, '', rest)


        except ValueError:
            # raise ValueError()
            salary_dict['unparsed'] = s

    elif s.startswith('от'):
        mask = r'\d+'
        reg = re.search(mask, s)
        salary_dict['min'] = reg[0]
        salary_dict['currency'] = re.sub('от' + mask, '', s)

    elif s.startswith('до'):
        mask = r'\d+'
        reg = re.search(mask, s)
        salary_dict['max'] = reg[0]
        salary_dict['currency'] = re.sub('до' + mask, '', s)

    else:
        salary_dict['unparsed'] = s
    return salary_dict

def get_page_number():

    pass


position_input = input('enter your desirable position: ')
POSITION = position_input if position_input else 'бездельник'       # if input is empty (по запросу 'бездельник' находит таки вакансии!!!!)
position = re.sub(' ', '+', POSITION)

browser = webdriver.Chrome(ChromeDriverManager().install())
# browser = webdriver.Chrome(ChromeDriverManager())  # TypeError: expected str, bytes or os.PathLike object, not ChromeDriverManager
# browser = webdriver.Chrome()  # WebDriverException

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}

base_url = [
    'https://www.hh.ru',
    'https://www.superjob.ru',
]

url = [
    base_url[0] + '/search/vacancy?area=2&fromSearchLine=true&text=' + position + '&from=suggest_post',
    # base_url[1] + '/.................',  # TODO
]

# Задаем принцип нумерации страниц,  номер первой страницы и кол-во вакансий на странице
pages = [
    ['&page=', 0, 50],
    ['&.......', 0, 10],  # TODO
]

vacancies_common_base = []

# MAIN
# цикл по сайтам-источникам
for n, source in enumerate(url):

    # первый пробный запрос для понимания общего кол-ва вакансий
    url_ = url[0] + pages[n][0] + str(0)
    # url_= 'https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&text=Python+junior&from=suggest_post&page=0'
    dom = get_response(url_, headers)

    # Общее кол-во вакансий
    vacancies_number = dom.find(attrs={'data-qa': 'vacancies-search-header'}).getText()  # TODO: актуально только для hh. Сделать универсально
    vacancies_number = re.sub(' ', '', vacancies_number)
    mask = r'^\d+'
    vacancies_number = re.search(mask, vacancies_number)[0]
    print(vacancies_number)

    vacancies_per_page = pages[n][2]
    MAX_PAGE = int(vacancies_number) // vacancies_per_page + 1

    while True:
        try:
            start_page_input = int(input(f'enter start page number (1 - {MAX_PAGE}): '))
            end_page_input = int(input(f'enter end page number ({start_page_input} - {MAX_PAGE}): '))
            break
        except (ValueError, TypeError):
            print('enter a number!!!')
            continue

    START_PAGE = int(start_page_input) if start_page_input else 1  # if input is empty
    END_PAGE = START_PAGE if (int(end_page_input) < START_PAGE) else int(end_page_input)
    END_PAGE = int(end_page_input) if end_page_input else START_PAGE  # if input is empty

    start_page = pages[0][1] + START_PAGE - 1
    end_page = END_PAGE - 1

    # цикл по страницам
    for page in range(start_page, end_page + 1):
        url_ = url[0] + pages[0][0] + str(page)
        dom = get_response(url_, headers)

        # Удаляет лишнюю хрень (hh.ru) (дамп размером 500к символов) TODO: неактуально для других источников
        for data in dom(['noindex']):
            # data.decompose()
            data.clear()

        vacancies = dom.find_all(vacancies_find)

        filename = str(page + 1) + '.html'
        with open(filename, 'w', encoding='utf-8') as f:
            # f.write(str(vacancies))
            f.write(str(dom.body))

        # парсим список вакансий и добавляем в словарь
        for vac in range(len(vacancies)):
            vacancies_common_base.append(vacancy_parsing(vacancies, vac))

# pprint(vacancies_common_base)

# for v in vacancies_common_base:
#     print(v['salary'])

with open('vacancies_common_base.json', 'w') as f:
    json.dump(vacancies_common_base, f)

with open('vacancies_common_base.json', 'r') as f:
    vacancies_common_base_readed = json.load(f)

print(' ============== vacancies_common_base_readed: ============== ')
pprint(vacancies_common_base_readed)

pprint(len(vacancies_common_base))

pass


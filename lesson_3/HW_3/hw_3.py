from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import DuplicateKeyError as dke
import re
import json


client = MongoClient('localhost', 27017)
db = client['vacancies_db']                 # database
vacancies = db.vacancies                    # collection

# DEBUG:
# vacancies.delete_many({})
# print("test: ", len(list(vacancies.find({}))))


# with open('/../../lesson_2/HW2/vacancies_common_base.json', 'r') as f:
with open('vacancies_common_base.json', 'r') as f:
    data = json.load(f)

# def str_to_int(s)


for vacancy in data:
    try:
        vacancy["_id"] = re.search('\d+$', vacancy['vacancy_link'])[0]
        # print(vacancy["_id"])
        if vacancy['salary'] != '---':
            if vacancy['salary'].get('min'):
                vacancy['salary']['min'] = int(vacancy['salary'].get('min'))
            if vacancy['salary'].get('max'):
                vacancy['salary']['max'] = int(vacancy['salary'].get('max'))

        # pprint(vacancy)
        vacancies.insert_one(vacancy)

        # break  # DEBUG
    except dke:
        pass

# print(len(data))


pprint("len=" + str(len(list(db.vacancies.find({})))))
# pprint(list(db.vacancies.find({})))


def salary_gt(amount):
    return list(vacancies.find({'$or': [
        {'salary.min': {'$gt': amount}},
        {'salary.max': {'$gt': amount}}
    ]}))
    # return vacancies.find({
    #     '_id': '51493055'
    # })


print('//'*100 + '\n')
x = salary_gt(220_000)
pprint(x)
print(len(x))


# pprint(list(vacancies.find({'salary.min': {'$gt': 250000}})))  # работает!
# pprint(list(vacancies.find({'salary.max': {'$gt': 250000}})))  # работает!
# print(list(vacancies.find({'salary': {'min': 300000}})))  # -------------
# pprint(list(vacancies.find({'salary.min': 300000})))   # работает!

# "salary"["max"]

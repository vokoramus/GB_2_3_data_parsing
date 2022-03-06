# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies0103

    def process_item(self, item, spider):
        # if spider.name == 'hhru':
        #     pass
        # else:
        #     pass
        #
        # item['min'], item['max'], item['cur'] = self.process_salary(item['salary'])
        # del item['salary']

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item



    def process_salary(self, salary):
        pass
        pass
        pass
        return 1,2,3
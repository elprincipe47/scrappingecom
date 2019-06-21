# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
import psycopg2

class Stroring:

    collection_name = 'scrapy_items'

    def __init__(self, mongodb, mongo_uri):
        self.mongodb = mongodb
        self.mongo_uri = mongo_uri

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self):
        self.client.close()

    def process_item(self, spider, item):
        self.db[self.collection_name].insert_one(dict(item))


class StoringPostgres:

    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = '***' # your password
        database = 'quotes'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self):
        self.client.close()

    def process_item(self, spider, item):
        self.cur.execute("insert into quotes_content(content,author) values(%s,%s)", (item['content'], item['author']))
        self.connection.commit()
        return item



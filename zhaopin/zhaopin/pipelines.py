# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ZhaoPinPipeline:
    def open_spider(self, spider):
        if spider.name == 'baidu':
            self.client = pymongo.MongoClient(host='localhost', port=27017)
            self.conn = self.client['zhaopin']['baidu_work']

    def process_item(self, item, spider):
        if spider.name == 'baidu':
            self.conn.insert_one(item)
            print('写入成功...')
        return item

    def close_spider(self, spider):
        if spider.name == 'baidu':
            self.client.close()

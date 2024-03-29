# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ZhaoPinPipeline:
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        if spider.name == 'baidu':
            self.conn = self.client['zhaopin']['baidu']
        if spider.name == 'tencent':
            self.conn = self.client['zhaopin']['tencent']
        if spider.name == 'aliyun':
            self.conn = self.client['zhaopin']['aliyun']
        if spider.name == 'taotian':
            self.conn = self.client['zhaopin']['taotian']

    def process_item(self, item, spider):
        self.conn.insert_one(item)
        print('写入成功...')
        # print(item)
        return item

    def close_spider(self, spider):
        self.client.close()

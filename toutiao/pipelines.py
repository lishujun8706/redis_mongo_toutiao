# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import uuid
import pymongo,time
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class ToutiaoPipeline(object):
    def __init__(self):
        connection=pymongo.MongoClient(host=settings['MONGOSERVER'],port=settings['MONGOPORT'])
        db=connection[settings['MONGODB']]
        self.collection=db[settings['MONGOCOLLECTION']]
    def process_item(self, item, spider):
        valid=True
        for data in item:
            if not data:
                valid=False
                raise DropItem("Missing {0}".format(data))
        if valid:
            print dict(item)
            print "@@@@@@@@@@@@@@@@@@@@&&&&&&&&&&&&&&&&@@@@@@@@@@"
            time.sleep(6)
            self.collection.insert(dict(item))
        # filename = uuid.uuid1()
        # with open('{}.txt'.format(filename),'w+') as f:
        #     f.write(item['content'].encode('utf-8'))
        # return item

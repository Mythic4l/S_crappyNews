# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from ssl import CERT_NONE
from hashlib import sha256
from scrapy.exceptions import DropItem


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, bbcspider):
        return cls(
            mongo_uri=bbcspider.settings.get("MONGO_URI"),
            mongo_db=bbcspider.settings.get("MONGO_DATABASE")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, ssl_cert_reqs=CERT_NONE)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if len(item["title"]) == 0:
            raise DropItem("Title is empty")

        if item["body"] is None:
            raise DropItem("Body is empty")

        if type(item["title"]) == list:
            item["title"] = item["title"][0]

        items = dict(item)
        items["checksum"] = sha256(item["body"]).hexdigest()

        # drop item if document exist
        query = {"checksum": items["checksum"]}
        if self.db.news.find(query).limit(1).count() > 0:
            raise DropItem("News exist")

        self.db.news.insert_one(items)
        return item
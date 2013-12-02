# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from .models import Session, create_comment


class MfaPipeline(object):
    def __init__(self):
        self.session = Session()

    def process_item(self, item, spider):
        if not item["images"]:
            raise DropItem
        create_comment(self.session, **item)
        return item

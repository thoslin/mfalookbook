# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MfaCommentItem(Item):
    post_url = Field()
    post_title = Field()
    post_timestamp = Field()
    permalink = Field()
    images = Field()
    point = Field()
    username = Field()
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from ..items import MfaItem


class MySpider(CrawlSpider):
    name = 'mfa'
    allowed_domains = ['reddit.com']
    start_urls = ['http://www.reddit.com/user/MFAModerator']

    rules = (
        Rule(SgmlLinkExtractor(
            restrict_xpaths="//a[contains(text(), 'WAYWT') and contains(@class, 'title')"
            " and contains(@href, 'waywt')]"),
            callback='parse_item'),
        Rule(SgmlLinkExtractor(restrict_xpaths="//a[contains(@rel, 'next') and contains(text(), 'next')]")),
    )

    def parse_item(self, response):
        sel = Selector(response)

        commentarea = sel.xpath('//div[@class="commentarea"]/div[3]')
        comments = commentarea.xpath("./div[contains(@class, 'thing') and contains(@class, 'comment')]")

        for comment in comments:
            item = MfaItem()
            item["url"] = response.url
            item["permalink"] = comment.xpath(".//a[text()='permalink']/@href")[0].extract()
            # TODO crawl dressed.so link
            item["images"] = [
                (link.xpath("@href").extract()[0], link.xpath("text()").extract()[0])
                for link in comment.xpath(".//a[contains(@href, 'imgur.com')]")]
            self.log(item)
            yield item
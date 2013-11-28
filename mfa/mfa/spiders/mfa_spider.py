from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from ..items import MfaCommentItem


class MySpider(CrawlSpider):
    name = 'mfa'
    allowed_domains = ['reddit.com']
    start_urls = ['http://www.reddit.com/user/MFAModerator']

    rules = (
        Rule(SgmlLinkExtractor(
            restrict_xpaths="//a[contains(text(), 'WAYWT') and contains(@class, 'title')"
            " and contains(@href, 'waywt')]", process_value=lambda url: url+"?limit=500"),
            callback='parse_item'),
        Rule(SgmlLinkExtractor(restrict_xpaths="//a[contains(@rel, 'next') and contains(text(), 'next')]")),
    )

    def parse_item(self, response):
        sel = Selector(response)

        post_url = response.url[:-10]
        post_timestamp = sel.xpath("//time/@datetime")[0].extract()

        sel_comment_area = sel.xpath('//div[@class="commentarea"]/div[3]')
        sel_comments = sel_comment_area.xpath("./div[contains(@class, 'thing') and contains(@class, 'comment')"
                                              " and not(contains(@class,'deleted'))]")

        for sel_comment in sel_comments:
            item = MfaCommentItem()

            item["post_url"] = post_url
            item["post_timestamp"] = post_timestamp
            item["permalink"] = sel_comment.xpath(".//a[text()='permalink']/@href")[0].extract()
            item["point"] = int(sel_comment.xpath(".//span[@class='score unvoted']/text()")[0].re(r"(\d+) point*")[0])
            # TODO crawl dressed.so link
            item["images"] = [
                (link.xpath("@href").extract()[0],
                 link.xpath("text()").extract()[0] if link.xpath("text()").extract() else "")
                for link in sel_comment.xpath(".//a[contains(@href, 'imgur.com')]")]
            self.log(item)

            yield item
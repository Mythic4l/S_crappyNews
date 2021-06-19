from abc import ABC

from scrapy.selector import Selector
from ..items import SpiderItems
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


def parse_item(response):
    item = SpiderItems()
    news = response.css('div.gs-c-promo-heading')
    for parson in news:

        item["url"] = response.url
        item["title"] = news.css('.gs-c-promo-heading__title::text').extract()
        item["body"] = news.css('.gs-c-promo-heading__summary::text').extract()

        yield item


class BbcSpider(CrawlSpider, ABC):
    name = "spider"
    allowed_domains = ["bbc.co.uk"]
    start_urls = ["http://www.bbc.co.uk/news"]
    rules = (
        Rule(LinkExtractor(allow=("",)), callback="parse_item"),
    )

    @staticmethod
    def __get_xpath_by_class(classname):
        """
        Get xpath syntax to search for classname
        :param classname: String
        :return: //*[contains(@class, 'classname')]
        """
        return "//*[contains(@class, '%s')]" % classname

from scrapy.selector import Selector
from S_crappyNews.items import SpiderItems
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BbcSpider(CrawlSpider):
    name = "bbcspider"
    allowed_domains = ["bbc.com"]
    start_urls = ["http://www.bbc.com/news"]
    rules = (
        Rule(LinkExtractor(allow=("",)), callback="parse_item"),
    )

    def parse_item(self, response):
        item = SpiderItems()
        item["url"] = response.url
        item["title"] = Selector(response=response).xpath(
            self.__get_xpath_by_class("story-body__h1") + "/text()").extract()
        item["body"] = " ".join(Selector(response=response).xpath(
            self.__get_xpath_by_class("story-body__inner") + "//p/text()").extract()).strip("\n")

        yield item

    @staticmethod
    def __get_xpath_by_class(classname):
        """
        Get xpath syntax to search for classname
        :param classname: String
        :return: //*[contains(@class, 'classname')]
        """
        return "//*[contains(@class, '%s')]" % classname

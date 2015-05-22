import scrapy
from items import WikiItem
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor


class WikiSpider(scrapy.Spider):
    name = "wikipeida"
    allowed_domains = ["wikipedia.org"]
    def __init__(self, **kw):
        super(WikiSpider, self).__init__(**kw)
        self.url = kw.get('url')
        self.allowed_domains = ["http://en.wikipedia.org"]
        self.link_extractor = LinkExtractor()


    def start_requests(self):
        return [Request(self.url, callback=self.parse, dont_filter=True)]

    def parse(self, response):
        title = Selector(response).xpath("//title/text()").extract()
        if title:
            item = WikiItem()
            item['title'] = title[0]
            print item['title']


import scrapy
import re
from urlparse import urlparse
from items import WikiItem
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor


class MultiLinkTitleSpider(scrapy.Spider):
    name = "wikipeida"
    json_line = " "
    def __init__(self, **kw):
        super(MultiLinkTitleSpider, self).__init__(**kw)
        self.url = kw.get('url')
        #self.allowed_domains = ["http://en.wikipedia.org"]
        self.allowed_domains = [re.sub(r'^www\.', '', urlparse(self.url).hostname)]
        self.link_extractor = LinkExtractor()


    def start_requests(self):
        return [Request(self.url, callback=self.parse, dont_filter=True)]

    def parse(self, response):
        title = Selector(response).xpath("//title/text()").extract()
        if title:
            item = WikiItem()
            item['title'] = title[0]
            print item['title']

        text = Selector(response).xpath("//div[@id='mw-content-text']/p/text() | //div[@id='mw-content-text']/p/b/text() | //div[@id='mw-content-text']/p/a/text()").extract()
        text_concat = "".join(text)
        text_concat.encode('ascii', errors='ignore')

        if text:
            item['description'] = text_concat[:500] + (text_concat[500:] and '..')

        print item['description']

        return item


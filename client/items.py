from scrapy.item import Item, Field

class WikiItem(Item):
    title = Field()
    text = Field()

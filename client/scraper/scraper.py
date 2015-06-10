import requests
import magpie_parser

class Scraper:
    def __init__(self, **kw):
        self.url = kw.get('url')
        self.parser = magpie_parser.MagpieParser

    def scrape_website(self):
        r = requests.get(self.url)
        return r.text



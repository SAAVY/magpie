import json
import re
import wikipedia
import lxml.html
from metadata import Metadata


class WikipediaMetadata(Metadata):

    prop_map = {}

    def parse_content(self, response):
        m = re.search(r"wiki\/(\S+)", response.url)
        title = m.group(1)
        document = lxml.html.fromstring(response.content)

        page = wikipedia.page(title)
        self.prop_map["description"] = page.summary
        self.prop_map["title"] = document.find(".//title").text
        self.prop_map["images"] = page.images[0:10] if len(page.images) > 9 else page.images
        return self.to_json(self.prop_map)

    def to_json(self, prop_map):
        return json.dumps(prop_map)

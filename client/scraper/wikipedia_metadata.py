import wikipedia
import lxml.html
from metadata import Metadata
import json


class WikipediaMetadata(Metadata):

    prop_map = {}

    def parse_content(self, content):
        document = lxml.html.fromstring(content)
        title = document.find(".//title").text

        page = wikipedia.page(title)
        self.prop_map["description"] = page.summary
        self.prop_map["title"] = title
        self.prop_map["image"] = page.images[0]
        return self.to_json(self.prop_map)

    def to_json(self, prop_map):
        return json.dumps(prop_map)

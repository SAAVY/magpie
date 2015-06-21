import json

import wikipedia
import lxml.html

from metadata import Metadata


class WikipediaMetadata(Metadata):

    prop_map = {}

    def parse_content(self, response):
        document = lxml.html.fromstring(response.content)
        title = document.find(".//title").text

        page = wikipedia.page(title)
        self.prop_map["description"] = page.summary
        self.prop_map["title"] = title
        self.prop_map["image"] = page.images[0]
        return self.to_json(self.prop_map)

    def to_json(self, prop_map):
        return json.dumps(prop_map)

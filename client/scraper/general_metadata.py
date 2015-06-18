from HTMLParser import HTMLParser
from metadata import Metadata
import json


class GeneralMetadata(Metadata, HTMLParser):
    json_return = ""
    prop_map = {}

    def parse_content(self, content):
        self.feed(content)
        return self.to_json(self.prop_map)

    def handle_starttag(self, tag, attrs):
        if tag == 'meta' and len(attrs) > 1:
            key = attrs[0][1]
            self.prop_map[key] = attrs[1][1]

    def to_json(self, prop_map):
        return json.dumps(prop_map)

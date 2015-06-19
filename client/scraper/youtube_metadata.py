import requests
from metadata import Metadata
import json
import urllib

request_url = "http://www.youtube.com/oembed?url="

class YoutubeMetadata(Metadata):
    prop_map = {}

    def parse_content(self, response):
        request = request_url + response.url
        resp = requests.get(request)
        data = resp.json()

        self.prop_map["html"] = urllib.quote(data["html"])
        self.prop_map["title"] = data["title"]
        self.prop_map["image"] = data["thumbnail_url"]
        return self.to_json(self.prop_map)

    def to_json(self, prop_map):
        return json.dumps(prop_map)

from client import config
from metadata import Metadata
import json
import requests
import re

request_url = "https://www.googleapis.com/drive/v2/files/"


class DriveMetadata(Metadata):
    prop_map = {}

    def parse_content(self, response):

        m = re.search(r"([-\w]{25,})", response.url)
        document_id = m.group()
        resp = requests.get(request_url + document_id + "?key=" + config.drive_api_key)
        data = resp.json()

        if data.get("error"):
            return self.to_json(data)

        self.prop_map["title"] = data["title"]
        self.prop_map["image"] = data["iconLink"]
        self.prop_map["ownerNames"] = data["ownerNames"]

        return self.to_json(self.prop_map)

    def to_json(self, prop_map):
        return json.dumps(prop_map)

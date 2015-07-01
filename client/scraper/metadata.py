import collections
import json

from flask import Response

from client.constants import FieldKeyword
from client.constants import StatusCode


class Metadata:

    def __init__(self, response):
        self.prop_map = collections.OrderedDict()
        self.prop_map[FieldKeyword.STATUS] = response.code
        self.prop_map[FieldKeyword.URL] = response.url
        self.prop_map[FieldKeyword.SANITIZED_URL] = response.sanitized_url
        self.parse_content(response)

    def parse_content(self, response):
        raise NotImplementedError("Every metadata scraper must implement parse_content")

    def to_json(self):
        json_data = json.dumps(self.prop_map)
        response = Response(response=json_data, status=StatusCode.OK, mimetype="application/json")
        return response

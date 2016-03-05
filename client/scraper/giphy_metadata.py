import collections
import json

from client.constants import FieldKeyword
from metadata import Metadata


class GiphyMetadata(Metadata):

    def get_title(self, response):
        return self.data_map[FieldKeyword.REQUEST_URL][6:].strip()

    def get_images_list(self, response):
        images_list = collections.OrderedDict()
        images_list[FieldKeyword.COUNT] = 0
        images_list[FieldKeyword.DATA] = []

        obj = json.loads(response.content)
        obj_data = obj['data']
        for i in obj_data:
            image_item_dict = collections.OrderedDict()
            image_item_dict[FieldKeyword.URL] = i['images']['fixed_height']['url']
            images_list[FieldKeyword.DATA].append(image_item_dict)
            images_list[FieldKeyword.COUNT] = images_list[FieldKeyword.COUNT] + 1
        if images_list[FieldKeyword.COUNT] > 0:
            return images_list
        return None

    def fetch_site_data(self, sanitized_url, status_code):
        return self.generic_fetch_content(sanitized_url, status_code)

    def parse_content(self, response):
        self.generic_parse_content(response)

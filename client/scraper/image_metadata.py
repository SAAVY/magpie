import collections

from client.constants import FieldKeyword
from metadata import Metadata


class ImageUrlMetadata(Metadata):

    def get_title(self, soup):
        image_url = self.prop_map[FieldKeyword.URL]
        return image_url.split('/')[-1]

    def get_images_list(self, soup):
        images_list = collections.OrderedDict()
        images_list[FieldKeyword.COUNT] = 1
        images_list[FieldKeyword.DATA] = []
        image_item_dict = collections.OrderedDict()
        image_item_dict[FieldKeyword.URL] = self.prop_map[FieldKeyword.URL]
        images_list[FieldKeyword.DATA].append(image_item_dict)
        return images_list

    def fetch_site_data(self, sanitized_url, status_code):
        return self.generic_fetch_content(sanitized_url, status_code)

    def parse_content(self, response):
        self.generic_parse_content(response)

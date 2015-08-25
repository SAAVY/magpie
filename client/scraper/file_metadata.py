import collections

from client.constants import FieldKeyword
from metadata import Metadata


class FileUrlMetadata(Metadata):

    def get_title(self, soup):
        image_url = self.prop_map[FieldKeyword.URL]
        return image_url.split('/')[-1]

    def get_files_list(self, response):
        file_list = collections.OrderedDict()
        file_list[FieldKeyword.COUNT] = 1
        file_list[FieldKeyword.DATA] = [{
            FieldKeyword.URL: response.request_url,
            FieldKeyword.TYPE: None
        }]

        return file_list

    def fetch_site_data(self, sanitized_url, status_code):
        return self.generic_fetch_content(sanitized_url, status_code)

    def parse_content(self, response):
        self.generic_parse_content(response)
        self.prop_map[FieldKeyword.FILES] = self.get_files_list(response)

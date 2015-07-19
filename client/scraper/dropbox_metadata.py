import collections
from urllib import urlencode
from urlparse import parse_qs
from urlparse import urlsplit
from urlparse import urlunsplit

from client.constants import FieldKeyword
from metadata import Metadata


class DropboxMetadata(Metadata):

    def fetch_site_data(self, sanitized_url, status_code):
        return self.generic_fetch_content(sanitized_url, status_code)

    def get_download_url(self, url):
        scheme, netloc, path, query_string, fragment = urlsplit(url)
        query_params = parse_qs(query_string)

        query_params["dl"] = "1"
        new_query_string = urlencode(query_params, doseq=True)

        return urlunsplit((scheme, netloc, path, new_query_string, fragment))

    def parse_content(self, response):
        self.generic_parse_content(response)

        file_list = collections.OrderedDict()
        file_list[FieldKeyword.COUNT] = 1
        file_list[FieldKeyword.DATA] = [
            {
                FieldKeyword.URL: self.get_download_url(response.sanitized_url),
                FieldKeyword.TYPE: None
            }]

        self.prop_map[FieldKeyword.FILES] = file_list

import collections
from urllib import urlencode
from urlparse import parse_qs, urlsplit, urlunsplit

from client.constants import FieldKeyword
from metadata import Metadata


class DropboxMetadata(Metadata):

    prop_map = {}

    def get_download_url(self, url):
        scheme, netloc, path, query_string, fragment = urlsplit(url)
        query_params = parse_qs(query_string)

        query_params["dl"] = "1"
        new_query_string = urlencode(query_params, doseq=True)

        return urlunsplit((scheme, netloc, path, new_query_string, fragment))

    def parse_content(self, response):
        self.general_parse_content(response)

        file_list = collections.OrderedDict()
        file_list[FieldKeyword.COUNT] = 1
        file_list[FieldKeyword.DATA] = [
            {
                FieldKeyword.URL: self.get_download_url(response.url),
                FieldKeyword.TYPE: None
            }]

        self.prop_map[FieldKeyword.FILES] = file_list

import collections
from urllib import urlencode
from urlparse import parse_qs
from urlparse import urlsplit
from urlparse import urlunsplit

from bs4 import BeautifulSoup

from client.constants import FieldKeyword
from client.constants import StatusCode
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
        soup = BeautifulSoup(response.content)
        title = self.get_title(soup)

        # TODO: currently unsure of how to tell if you have landed on a page that has 404ed since dropbox always returns 200 status
        # the below is a hack to get around this problem, will need to clean this up once we've figured out how to resolve this issue
        if title == 'Dropbox - Error':
            self.prop_map[FieldKeyword.STATUS] = StatusCode.NOT_FOUND
            self.prop_map[FieldKeyword.ERROR_MSG] = StatusCode.get_status_message(StatusCode.NOT_FOUND)

            favicon_url = self.get_favicon_url(soup)
            desc = self.get_desc(soup)

            self.prop_map[FieldKeyword.TITLE] = title
            self.prop_map[FieldKeyword.FAVICON] = favicon_url
            self.prop_map[FieldKeyword.DESC] = desc

        else:
            self.generic_parse_content(response)

            file_list = collections.OrderedDict()
            file_list[FieldKeyword.COUNT] = 1
            file_list[FieldKeyword.DATA] = [
                {
                    FieldKeyword.URL: self.get_download_url(response.url),
                    FieldKeyword.TYPE: None
                }]

            self.prop_map[FieldKeyword.FILES] = file_list

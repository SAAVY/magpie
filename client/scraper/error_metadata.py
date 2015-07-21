from bs4 import BeautifulSoup

from client import url_utils
from client.constants import FieldKeyword
from client.constants import StatusCode
from client.response import Response
from metadata import Metadata


class ErrorMetadata(Metadata):

    def fetch_site_data(self, sanitized_url, status_code):
        response = None
        if status_code is not StatusCode.BAD_REQUEST:
            response = self.generic_fetch_content(sanitized_url, status_code)
            status_code = response.status_code
        else:
            response = Response()
        status_code, error_msg = url_utils.get_error(status_code)
        response.set_error(status_code, error_msg)
        return response

    def parse_content(self, response):
        self.prop_map[FieldKeyword.STATUS] = response.status_code
        self.prop_map[FieldKeyword.ERROR_MSG] = response.error_msg

        soup = BeautifulSoup(response.content)
        title = self.get_title(soup)
        desc = self.get_desc(soup)
        favicon_url = self.get_favicon_url(soup)

        self.prop_map[FieldKeyword.TITLE] = title

        self.prop_map[FieldKeyword.DESC] = desc

        self.prop_map[FieldKeyword.FAVICON] = favicon_url
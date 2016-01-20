from flask import current_app

from client import url_utils
from client.constants import FieldKeyword
from client.constants import StatusCode
from client.response import Response
from metadata import Metadata


class ErrorMetadata(Metadata):

    def init_fields(self):
        self.prop_map[FieldKeyword.STATUS] = None
        self.prop_map[FieldKeyword.ERROR_MSG] = None
        self.prop_map[FieldKeyword.URL] = None
        self.prop_map[FieldKeyword.REQUEST_URL] = None
        self.prop_map[FieldKeyword.PROVIDER_URL] = None
        self.prop_map[FieldKeyword.TITLE] = None
        self.prop_map[FieldKeyword.DESC] = None

    def fetch_site_data(self, sanitized_url, status_code):
        logger = current_app.logger
        response = None
        if status_code != StatusCode.BAD_REQUEST:
            response = self.generic_fetch_content(sanitized_url, status_code)
            status_code = response.status_code
        else:
            response = Response()
        status_code, error_msg = url_utils.get_error(status_code)
        response.set_error(status_code, error_msg)
        logger.warn("fetch_site_data, error_msg: %s, status_code: %d, sanitized_url: %s", error_msg, status_code, sanitized_url)
        return response

    def parse_content(self, response):
        self.prop_map[FieldKeyword.STATUS] = response.status_code
        self.prop_map[FieldKeyword.ERROR_MSG] = response.error_msg

        if response.status_code != StatusCode.BAD_REQUEST:
            self.generic_parse_content(response)

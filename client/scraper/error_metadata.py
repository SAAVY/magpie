from client.constants import FieldKeyword
from metadata import Metadata


class ErrorMetadata(Metadata):

    def parse_content(self, response):
        self.prop_map[FieldKeyword.STATUS] = response.code
        self.prop_map[FieldKeyword.ERROR_MSG] = response.error_msg

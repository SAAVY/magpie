from urlparse import urlparse
import collections
import re

from client.constants import FieldKeyword
from client.constants import FileTypeValue
from metadata import Metadata

api_request_url = "https://www.googleapis.com/drive/v2/files/"
docs_request_url = "https://docs.google.com/"
export_presentation_path = "/export/pdf"
export_path = "/export?format=pdf"


class DriveMetadata(Metadata):

    def fetch_site_data(self, sanitized_url, status_code):
        return self.generic_fetch_content(sanitized_url, status_code)

    def get_download_url(self, url):
        parsed_url = urlparse(url)
        m = re.search(r"([-\w]{25,})", parsed_url.path)
        document_id = m.group()

        m = re.search(r"\/(\w*)\/", parsed_url.path)
        doc_type = m.group(1)

        if doc_type == "presentation":
            export_url = docs_request_url + doc_type + "/d/" + document_id + export_presentation_path
        else:
            export_url = docs_request_url + doc_type + "/d/" + document_id + export_path

        return export_url

    def parse_content(self, response):
        self.generic_parse_content(response)

        file_list = collections.OrderedDict()
        file_list[FieldKeyword.COUNT] = 1
        file_list[FieldKeyword.DATA] = [
            {
                FieldKeyword.URL: self.get_download_url(response.url),
                FieldKeyword.TYPE: FileTypeValue.PDF
            }]

        self.prop_map[FieldKeyword.FILES] = file_list

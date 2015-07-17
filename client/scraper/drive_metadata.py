import collections
import re

from client.constants import FieldKeyword
from client.constants import FileTypeValue
from metadata import Metadata

request_url = "https://www.googleapis.com/drive/v2/files/"
docs_url = "https://docs.google.com/"


class DriveMetadata(Metadata):
    prop_map = {}

    def get_download_url(self, url):
        m = re.search(r"([-\w]{25,})", url)
        document_id = m.group()

        m = re.search(r".com\/(\w*)\/", url)
        doc_type = m.group(1)

        if doc_type == "presentation":
            export_url = docs_url + doc_type + "/d/" + document_id + "/export/pdf"
        else:
            export_url = docs_url + doc_type + "/d/" + document_id + "/export?format=pdf"

        return export_url

    def parse_content(self, response):
        self.general_parse_content(response)

        file_list = collections.OrderedDict()
        file_list[FieldKeyword.DATA] = [
            {
                FieldKeyword.URL: self.get_download_url(response.url),
                FieldKeyword.TYPE: FileTypeValue.PDF
            }]
        file_list[FieldKeyword.COUNT] = 1

        self.prop_map[FieldKeyword.FILES] = file_list

from metadata import Metadata


class GeneralMetadata(Metadata):

    def fetch_site_data(self, sanitized_url, status_code):
        return self.generic_fetch_content(sanitized_url, status_code)

    def parse_content(self, response, tag_id, tag_class, tag_name):
        self.tag_id = tag_id
        self.tag_class = tag_class
        self.tag_name = tag_name
        self.generic_parse_content(response)

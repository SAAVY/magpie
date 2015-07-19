from metadata import Metadata


class GeneralMetadata(Metadata):

    def fetch_site_data(self, sanitized_url, status_code):
        return self.generic_fetch_content(sanitized_url, status_code)

    def parse_content(self, response):
        self.generic_parse_content(response)

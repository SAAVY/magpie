from metadata import Metadata


class GeneralMetadata(Metadata):

    def parse_content(self, response):
        self.general_parse_content(response)

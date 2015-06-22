class Metadata:

    def parse_content(self, response):
        raise NotImplementedError("Every metadata scraper must implement parse_content")

    def to_json(self, prop_map):
        raise NotImplementedError("Every metadata scraper must implement to_json")

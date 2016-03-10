from constants import ResponseType
from config import config


class QueryParams:

    def __init__(self):
        self.response_type = ResponseType.JSON
        self.desc_length = config.MAX_DESC_LENGTH
        self.query_urls = None

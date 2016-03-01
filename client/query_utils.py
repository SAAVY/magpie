from constants import ResponseType
from config import MAX_DESC_LENGTH


class QueryParams:

    def __init__(self):
        self.response_type = ResponseType.JSON
        self.desc_length = MAX_DESC_LENGTH
        self.query_url = None

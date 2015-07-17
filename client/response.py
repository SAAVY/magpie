from client.constants import StatusCode


class Response:
    def __init__(self):
        self.code = None
        self.content = None
        self.error_msg = None
        self.header = None
        self.response_code = None
        self.sanitized_url = None
        self.type = None
        self.url = None
        self.domain_url = None

    def set_content(self, header, content, code, url, sanitized_url, type, domain_url):
        self.code = StatusCode.OK
        self.content = content
        self.header = header
        self.response_code = code
        self.sanitized_url = sanitized_url
        self.type = type
        self.url = url
        self.domain_url = domain_url

    def set_error(self, code, error_msg, url):
        self.code = code
        self.error_msg = error_msg
        self.url = url

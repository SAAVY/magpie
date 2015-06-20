class Response:
    def __init__(self):
        self.code = None
        self.content = None
        self.error_msg = None
        self.header = None
        self.response_code = None
        self.url = None
        self.type = None

    def set_content(self, header, content, code, url, type):
        self.content = content
        self.header = header
        self.response_code = code
        self.url = url
        self.type = type

    def set_error(self, code, error_msg):
        self.code = code
        self.error_msg = error_msg

class Response:
    def __init__(self):
        self.code = None
        self.content = None
        self.error_msg = None
        self.header = None
        self.response_code = None
        self.url = None
    
    def set_content(self, header, content, code, url):
        self.content = content
        self.header = header
        self.response_code = code
        self.url = url

    def set_error(self, code, error_msg):
        self.code = code
        self.error_msg = error_msg

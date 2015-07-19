class Response:
    def __init__(self):
        self.content = None
        self.provider_url = None
        self.error_msg = None
        self.header = None
        self.status_code = None
        self.sanitized_url = None
        self.url = None
        self.wiki_page = None

    def set_content(self, header, content, code, sanitized_url, provider_url):
        self.content = content
        self.header = header
        self.status_code = code
        self.sanitized_url = sanitized_url
        self.provider_url = provider_url

    def set_wiki_content(self, wiki_page):
        self.wiki_page = wiki_page

    def set_error(self, code, error_msg):
        self.status_code = code
        self.error_msg = error_msg

class Response:
    def __init__(self):
        self.api_content = None
        self.api_url = None
        self.content = None
        self.error_msg = None
        self.header = None
        self.provider_url = None
        self.request_url = None
        self.status_code = None
        self.url = None
        self.wiki_page = None

    def set_content(self, header, content, code, request_url, provider_url):
        self.content = content
        self.header = header
        self.status_code = code
        self.request_url = request_url
        self.provider_url = provider_url

    def set_api_content(self, api_content):
        self.api_content = api_content

    def set_wiki_content(self, wiki_page):
        self.wiki_page = wiki_page

    def set_error(self, code, error_msg):
        self.status_code = code
        self.error_msg = error_msg

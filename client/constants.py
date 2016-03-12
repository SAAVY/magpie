LOCALHOST = "127.0.0.1"

# This is a public api key, as found in https://github.com/Giphy/GiphyAPI
GIPHY_API_KEY = "dc6zaTOxFJmzC"


class StatusCode(object):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    RATE_LIMIT = 429
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503
    WEBSITE_REQUEST_ERROR = 550
    REQUEST_TIMEOUT = 408

    status_codes = {OK: "OK",
                    NOT_FOUND: "Page Not Found",
                    INTERNAL_SERVER_ERROR: "Internal Server Error",
                    SERVICE_UNAVAILABLE: "Service Unavailable",
                    BAD_REQUEST: "Bad Request",
                    UNAUTHORIZED: "Unauthorized",
                    RATE_LIMIT: "Too Many Requests",
                    FORBIDDEN: "Forbidden",
                    WEBSITE_REQUEST_ERROR: "Website Request Error",
                    REQUEST_TIMEOUT: "Request Timeout"}

    @staticmethod
    def get_status_message(code):
        return StatusCode.status_codes.get(code)


class UrlTypes(object):
    GDRIVE = "drive.google.com"
    DROPBOX = "dropbox.com"
    GENERAL = "general"
    WIKI = "wikipedia.org"
    YOUTUBE = "youtube.com"
    GDOCS = "docs.google.com"
    ERROR = "error"
    DIRECT_IMAGE = "image/"
    DIRECT_FILE = "application/"
    GIPHY_API = "api.giphy.com"


class FieldKeyword(object):
    API_QUERY_URL = "api_query_url"  # if an api was used, api_query_url is the request url used
    COUNT = "count"
    DATA = "data"
    DESC = "description"
    ERROR_MSG = "error_message"
    EXTRACT = "extract"
    FROM_CACHE = "from_cache"
    FAVICON = "favicon"
    FILES = "files"
    HEIGHT = "height"
    HTML = "html"
    IMAGES = "images"
    MEDIA = "media"
    PROVIDER_URL = "provider_url"
    REQUEST_URL = "request_url"
    SOURCE = "source"
    STATUS = "status"
    THUMBNAIL = "thumbnail"
    TITLE = "title"
    TYPE = "type"
    URL = "url"
    WIDTH = "width"
    IFRAME = "iframe"


class MediaTypeValue(object):
    IMAGE = "image"
    VIDEO = "video"


class FileTypeValue(object):
    NONE = "none"
    PDF = "pdf"


class MetadataFields(object):
    IFRAME = "iframe"
    CONTENT = "content"
    DESCRIPTION = "description"
    IMAGE = "img"
    HEIGHT = "height"
    LINK = "link"
    META = "meta"
    NAME = "name"
    OG_DESC = "og:description"
    OG_IMAGE = "og:image"
    OG_TITLE = "og:title"
    PROPERTY = "property"
    REL = "rel"
    SRC = "src"
    TITLE = "title"
    TYPE = "type"
    WIDTH = "width"


class ResponseType(object):
    JSON = "json"

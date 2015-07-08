class StatusCode(object):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

    status_codes = {OK: "OK",
                    NOT_FOUND: "Not Found",
                    INTERNAL_SERVER_ERROR: "Internal Server Error",
                    BAD_REQUEST: "Bad Request",
                    UNAUTHORIZED: "Unauthorized"}

    @staticmethod
    def get_status_message(code):
        return StatusCode.status_codes.get(code)


class UrlTypes(object):

    DRIVE = "google drive"
    DROPBOX = "dropbox"
    GENERAL = "general"
    WIKI = "wikipedia"
    YOUTUBE = "youtube"
    DOCS = "google docs"

    special_urls = {
        DOCS: "docs.google.com",
        DROPBOX: "dropbox.com",
        WIKI: "wikipedia.org",
        YOUTUBE: "youtube.com"
    }

    @staticmethod
    def get_special_url(url_type):
        return UrlTypes.special_urls.get(url_type)


class FieldKeyword(object):
    COUNT = "count"
    DATA = "data"
    DESC = "description"
    DOWNLOAD_URL = "download_url"
    ERROR_MSG = "error_message"
    FILES = "files"
    IFRAME = "iframe"
    MEDIA = "media"
    SANITIZED_URL = "sanitized_url"
    SRC = "source"
    STATUS = "status"
    TITLE = "title"
    TYPE = "type"
    URL = "url"


class MediaTypeValue(object):
    IMAGE = "image"
    VIDEO = "video"


class FileTypeValue(object):
    NONE = "none"
    PDF = "pdf"


class MetadataFields(object):
    DESCRIPTION = "description"
    NAME = "name"
    OG_DESC = "og:description"
    OG_IMAGE = "og:image"
    OG_TITLE = "og:title"
    PROPERTY = "property"
    TITLE = "title"


class ResponseType(object):
    JSON = "json"

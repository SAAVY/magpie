class StatusCode(object):
    OK = 200
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    BAD_REQUEST = 400
    UNAUTHORIZED = 401


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
    DROP_BOX = "dropbox"
    GENERAL = "general"
    WIKI = "wikipedia"
    YOUTUBE = "youtube"

    special_urls = {
        WIKI: "en.wikipedia.org",
        YOUTUBE: "youtube.com"
    }

    @staticmethod
    def get_special_url(url_type):
        return UrlTypes.special_urls.get(url_type)

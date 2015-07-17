import re  # regular expressions
import requests
from urlparse import urlparse

from constants import StatusCode
from constants import UrlTypes
from response import Response


def get_url_data(url):
    sanitized_url = validate_url(url)
    url_type = get_url_type(sanitized_url)
    response = Response()
    try:
        request = requests.get(sanitized_url)
        # TODO (Alice): differentiate different request data codes (404 etc)
        # Passing in request.content (it's in bytes rather than unicode - which is what request.text gives)
        response.set_content(request.headers, request.content, request.status_code, url, sanitized_url, url_type)
    except Exception:
        response.set_error(StatusCode.BAD_REQUEST, StatusCode.get_status_message(StatusCode.BAD_REQUEST), url)
    finally:
        pass

    return response


def validate_url(url):
    parsed_url = urlparse(url)
    if not re.match('(http|https)', parsed_url.scheme):
        url = 'http://' + url
        parsed_url = urlparse(url)

    return parsed_url.geturl()


def get_url_type(url):
    if UrlTypes.get_special_url(UrlTypes.DOCS) in url:
        return UrlTypes.DOCS
    elif UrlTypes.get_special_url(UrlTypes.DROPBOX) in url:
        return UrlTypes.DROPBOX
    elif UrlTypes.get_special_url(UrlTypes.WIKI) in url:
        return UrlTypes.WIKI
    elif UrlTypes.get_special_url(UrlTypes.YOUTUBE) in url:
        return UrlTypes.YOUTUBE
    else:
        return UrlTypes.GENERAL

from urlparse import urlparse
import re
import requests
from response import Response
from constants import StatusCode, UrlTypes


def get_url_data(url):
    url = validate_url(url)
    url_type = get_url_type(url)
    response = Response()
    try:
        request = requests.get(url)
        # TODO (Alice): differentiate different request data codes (404 etc)
        # Passing in request.content (it's in bytes rather than unicode - which is what request.text gives)
        response.set_content(request.headers, request.content, request.status_code, url, url_type)
    except Exception:
        response.set_error(StatusCode.BAD_REQUEST, StatusCode.get_status_message(StatusCode.BAD_REQUEST))
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
    if UrlTypes.get_special_url(UrlTypes.WIKI) in url:
        return UrlTypes.WIKI
    else:
        return UrlTypes.GENERAL

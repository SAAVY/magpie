import re  # regular expressions
import requests
from urlparse import urlparse

from constants import StatusCode
from constants import UrlTypes
from response import Response


def get_url_data(url):
    sanitized_url = sanitize_url(url)
    response = Response()
    try:
        url_type = get_url_type(sanitized_url)
        request = requests.get(sanitized_url)
        sanitized_url = request.url
        domain_url = get_domain_url(sanitized_url)

        print request
        print request.url
        # TODO (Alice): differentiate different request data codes (404 etc)
        # Passing in request.content (it's in bytes rather than unicode - which is what request.text gives)
        response.set_content(request.headers, request.content, request.status_code, url, sanitized_url, url_type, domain_url)
    except Exception:
        response.set_error(StatusCode.BAD_REQUEST, StatusCode.get_status_message(StatusCode.BAD_REQUEST), url)
    finally:
        pass

    return response


def sanitize_url(url):
    parsed_url = urlparse(url)
    if not re.match('(http|https)', parsed_url.scheme):
        url = 'http://' + url
        parsed_url = urlparse(url)

    return parsed_url.geturl()


def get_domain_url(url):
    parsed_uri = urlparse(url)
    domain_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain_url


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

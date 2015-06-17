from httplib import HTTP
from urlparse import urlparse
import httplib
import re
import requests
import urllib2

from response import Response
from constants import StatusCode


def get_url_data(url):
    url = validate_url(url)

    response = Response()
    try:
        request = requests.get(url)
        # TODO (Alice): differentiate different request data codes (404 etc)
        response.set_content(request.headers, request.text, request.status_code, url)
    except Exception, e:
        response.set_error(StatusCode.BAD_REQUEST, StatusCode.get_status_message(BAD_REQUEST))
    finally:
        pass

    return response

def validate_url(url):
    parsed_url = urlparse(url)
    if not re.match('(http|https)', parsed_url.scheme):
        url = 'http://' + url
        parsed_url = urlparse(url)

    return parsed_url.geturl()



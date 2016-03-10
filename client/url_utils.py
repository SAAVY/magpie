import re  # regular expressions
from urlparse import urlparse
from urlparse import urlunparse

from flask import current_app
import httplib
import requests

import blacklist
from config import config
from constants import StatusCode
from constants import UrlTypes
from constants import MetadataFields


def http_get_response_patch(self, *args, **kwargs):
    response = _old_getresponse(self, *args, **kwargs)
    if self.sock:
        response.peer = self.sock.getpeername()
        ip_address = response.peer[0]
        port = response.peer[1]
        if blacklist.is_website_blacklisted(ip_address, port):
            return None
    else:
        response.peer = None
    return response

_old_getresponse = httplib.HTTPConnection.getresponse
httplib.HTTPConnection.getresponse = http_get_response_patch


def get_requests_header(url):
    logger = current_app.logger
    head = None
    try:
        head = requests.head(url, allow_redirects=True, stream=True)
        peer = head.raw._fp.fp._sock.getpeername()
        ip_address = peer[0]
        port = peer[1]
        if blacklist.is_website_blacklisted(ip_address, port):
            return None
    except AttributeError as e:
        logger.exception("get_requests_header AttributeError: %s" % str(e))
    except Exception as e:
        logger.exception("get_requests_header Exception: %s" % str(e))
    return head


def get_requests_content(url):
    logger = current_app.logger
    response = None
    try:
        response = requests.get(url, allow_redirects=True)
    except AttributeError as e:
        logger.exception("get_requests_header AttributeError: %s" % str(e))
    except Exception as e:
        logger.exception("get_requests_header Exception: %s" % str(e))
    return response.content


def get_redirect_url(head):
    if head is not None:
        return head.url
    return None


def get_content_type(head):
    if head is not None:
        content_type = head.headers['content-type']
        return content_type
    return None


def get_error(status_code):
    if status_code is None or status_code == StatusCode.BAD_REQUEST:
        return StatusCode.BAD_REQUEST, StatusCode.get_status_message(StatusCode.BAD_REQUEST)
    if status_code == StatusCode.UNAUTHORIZED:
        return StatusCode.UNAUTHORIZED, StatusCode.get_status_message(StatusCode.UNAUTHORIZED)
    if status_code == StatusCode.FORBIDDEN:
        return StatusCode.FORBIDDEN, StatusCode.get_status_message(StatusCode.FORBIDDEN)
    if status_code == StatusCode.NOT_FOUND:
        return StatusCode.NOT_FOUND, StatusCode.get_status_message(StatusCode.NOT_FOUND)
    if status_code == StatusCode.INTERNAL_SERVER_ERROR:
        return StatusCode.INTERNAL_SERVER_ERROR, StatusCode.get_status_message(StatusCode.INTERNAL_SERVER_ERROR)
    return StatusCode.OK, None


def sanitize_url(url):
    if(url.lower().startswith('/giphy')):
        query_p1 = "http://api.giphy.com/v1/gifs/search?q="
        query_p3 = "&api_key=dc6zaTOxFJmzC&limit=10"
        search = url[7:].strip().replace(" ", "+")
        return query_p1 + search + query_p3

    parsed_url = urlparse(url)
    if not re.match('(http|https)', parsed_url.scheme):
        url = 'http://' + url
        parsed_url = urlparse(url)

    sanitized_url = remove_url_fragments(parsed_url.geturl())
    return sanitized_url


def remove_url_fragments(url):
    scheme, netloc, path, params, query, fragment = urlparse(url)
    parsed_url = urlunparse((scheme, netloc, path, params, query, ""))
    return parsed_url


def remove_url_queries(url):
    scheme, netloc, path, params, query, fragment = urlparse(url)
    parsed_url = urlunparse((scheme, netloc, path, params, "", fragment))
    return parsed_url


def get_domain_url(url):
    parsed_uri = urlparse(url)
    provider_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return provider_url


def validate_image_url(image_url, provider_url, request_head=False, optional_path=None):
    parsed_image_uri = urlparse(image_url)
    parsed_provider_uri = urlparse(provider_url)
    path = parsed_image_uri.path
    netloc = parsed_image_uri.netloc
    scheme = parsed_image_uri.scheme
    if image_url.startswith(parsed_provider_uri.netloc):
        path = path[len(parsed_provider_uri.netloc):]
    if not netloc:
        netloc = parsed_provider_uri.netloc
    if not scheme:
        scheme = parsed_provider_uri.scheme
    if not path or path == "/":
        path = optional_path
    if not (scheme and netloc and path):
        return None  # ERROR cannot parse image url
    image_url = urlunparse((scheme, netloc, path, "", "", ""))
    if request_head:
        head = get_requests_header(image_url)
        if head is None:
            return None  # ERROR image is invalid
    return image_url.encode('utf-8')


def validate_image_dimensions(image):
    if (image.has_attr(MetadataFields.HEIGHT) and int(image[MetadataFields.HEIGHT]) <
            config.ImageAttrs.MIN_IMAGE_HEIGHT):
        return False
    if (image.has_attr(MetadataFields.WIDTH) and int(image[MetadataFields.WIDTH]) <
            config.ImageAttrs.MIN_IMAGE_WIDTH):
        return False
    return True


def get_url_type(url, status_code, content_type):
    error_code, error_msg = get_error(status_code)
    if error_code != StatusCode.OK:
        return UrlTypes.ERROR
    parsed_url = urlparse(url)
    netloc_url = parsed_url.netloc
    if UrlTypes.GIPHY_API in netloc_url:
        return UrlTypes.GIPHY_API
    if content_type.startswith(UrlTypes.DIRECT_IMAGE):
        return UrlTypes.DIRECT_IMAGE
    if content_type.startswith(UrlTypes.DIRECT_FILE):
        return UrlTypes.DIRECT_FILE
    if UrlTypes.GDOCS in netloc_url:
        return UrlTypes.GDOCS
    if UrlTypes.DROPBOX in netloc_url:
        return UrlTypes.DROPBOX
    if UrlTypes.WIKI in netloc_url:
        return UrlTypes.WIKI
    if UrlTypes.YOUTUBE in netloc_url:
        return UrlTypes.YOUTUBE
    return UrlTypes.GENERAL

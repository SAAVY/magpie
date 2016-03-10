from flask import current_app
from flask import Response as FlaskResponse

import cache_utils
from config import config
import collections
from constants import FieldKeyword
from constants import StatusCode
from constants import UrlTypes
import format_utils
import json
from scraper import drive_metadata
from scraper import dropbox_metadata
from scraper import error_metadata
from scraper import file_metadata
from scraper import general_metadata
from scraper import image_metadata
from scraper import wikipedia_metadata
from scraper import youtube_metadata
from scraper import giphy_metadata
import url_utils
from url_utils import BlacklistUrlException


def get_logger():
    return current_app.logger


def get_url_metadata(query_params, return_error=False):
    if return_error:
        return generate_bad_request_response()

    logger = get_logger()
    desc_length = query_params.desc_length
    response_type = query_params.response_type
    url = query_params.query_urls[0].strip()

    try:
        metadata = get_metadata(url, response_type, desc_length)
    except BlacklistUrlException as e:
        logger.warn("BlacklistUrlException: %s " % str(e))
        return generate_bad_request_response("Invalid url requested")
    response = FlaskResponse(response=metadata, status=StatusCode.OK, mimetype="application/json")
    return response


def get_urls_metadata(query_params, return_error=False):
    if return_error:
        return generate_bad_request_response()

    logger = get_logger()
    urls = query_params.query_urls
    desc_length = query_params.desc_length
    response_type = query_params.response_type

    json_output = collections.OrderedDict()
    json_output['response_count'] = len(urls)
    json_output['responses'] = []
    try:
        for url in urls:
            metadata = get_metadata(url.strip(), response_type, desc_length)
            json_output['responses'].append(json.loads(metadata))
    except BlacklistUrlException as e:
        logger.warn("BlacklistUrlException: %s " % str(e))
        return generate_bad_request_response("Invalid url requested")
    multiple_responses = get_json_metadata(json_output)
    response = FlaskResponse(response=multiple_responses, status=StatusCode.OK, mimetype="application/json")
    return response


def generate_rate_limit_response():
    data = {"error": "Rate limit exceeded"}
    response = FlaskResponse(response=json.dumps(data), status=StatusCode.RATE_LIMIT, mimetype="application/json")
    return response


def generate_bad_request_response(error_msg="Invalid request"):
    data = {"error": error_msg}
    response = FlaskResponse(response=json.dumps(data), status=StatusCode.BAD_REQUEST, mimetype="application/json")
    return response


def get_cached_data(url):
    """
    Get cached data for url
    """
    logger = get_logger()
    data = cache_utils.get_cached_data(url)   # If data from db is None, continue and parse the website
    if data is not None:
        logger.debug("FUNC: get_cached_data, Cache hit for key %s", url)
        data_map = json.loads(data.metadata)
        json_data = {}
        json_data[FieldKeyword.REQUEST_URL] = url
        json_data[FieldKeyword.FROM_CACHE] = True
        json_data[FieldKeyword.DATA] = data_map
        return json_data
    return None


def get_metadata(url, response_type, desc_length):
    metadata = None
    content_type = None
    response_code = None
    logger = get_logger()
    logger.debug("FUNC: get_metadata, url: %s, response_type: %s" % (url, response_type))
    sanitized_url = url_utils.sanitize_url(url)
    logger.debug("Sanitized url: %s" % sanitized_url)

    if config.CACHE_DATA:
        json_data = get_cached_data(url)
        if json_data:
            return get_json_metadata(json_data)

    head = url_utils.get_requests_header(sanitized_url)

    if head is None:
        return generate_error_metadata(url)
    else:
        sanitized_url = url_utils.get_redirect_url(head)
        content_type = url_utils.get_content_type(head)
        response_code = head.status_code
        metadata = create_metadata_object(url, response_code, sanitized_url, content_type)

    # Check for caching, otherwise proceed with scraping
    if config.CACHE_DATA:
        data = cache_utils.get_cached_data(sanitized_url)   # If data from db is None, continue and parse the website
        if data is not None:
            logger.debug("Cache hit for key %s", sanitized_url)
            data_map = json.loads(data.metadata)
            metadata.data_map[FieldKeyword.FROM_CACHE] = True
            metadata.data_map[FieldKeyword.DATA] = data_map
            return get_json_metadata(metadata.data_map)

    site_response = metadata.fetch_site_data(sanitized_url, response_code)

    metadata.parse_content(site_response)
    metadata.data_map[FieldKeyword.FROM_CACHE] = False

    # Trim the description if necessary
    format_utils.trim_description(metadata, desc_length)

    json_data = get_json_metadata(metadata.data_map)
    logger.info(json_data)
    if config.CACHE_DATA and site_response.status_code == StatusCode.OK:
        cache_map = metadata.get_cache_prop_map()
        cache_data = get_json_metadata(cache_map)
        logger.debug("Caching json data to redis db")
        cache_utils.cache_json_data(sanitized_url, cache_data)

    return json_data


def generate_error_metadata(url):
    response_code = StatusCode.BAD_REQUEST
    metadata = create_metadata_object(url, StatusCode.BAD_REQUEST, None, None)
    site_response = metadata.fetch_site_data(url, response_code)
    status_code, error_msg = url_utils.get_error(response_code)
    site_response.set_error(status_code, error_msg)
    metadata.parse_content(site_response)

    return get_json_metadata(metadata.data_map)


def get_json_metadata(map):
    return format_utils.to_json(map)


def create_metadata_object(url, response_code, sanitized_url, content_type):
    logger = get_logger()
    logger.debug("FUNC: create_metadata_object, URL: %s, response_code: %d, sanitized_url: %s, content_type: %s" %
                 (url, response_code, sanitized_url, content_type))
    url_type = url_utils.get_url_type(sanitized_url, response_code, content_type)
    if url_type is UrlTypes.ERROR:
        return error_metadata.ErrorMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.GDOCS:
        return drive_metadata.DriveMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.DROPBOX:
        return dropbox_metadata.DropboxMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.WIKI:
        return wikipedia_metadata.WikipediaMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.YOUTUBE:
        return youtube_metadata.YoutubeMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.DIRECT_IMAGE:
        return image_metadata.ImageUrlMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.DIRECT_FILE:
        return file_metadata.FileUrlMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.GIPHY_API:
        return giphy_metadata.GiphyMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.GENERAL:
        return general_metadata.GeneralMetadata(url, response_code, sanitized_url)
    return None

import logging

from flask import current_app
from flask import Response as FlaskResponse

import cache_utils
import config
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
import url_utils
from utils.profile import cprofile


@cprofile
def get_metadata(query_params):
    url = query_params.query_url
    desc_length = query_params.desc_length
    response_type = query_params.response_type

    logger = current_app.logger
    logger.setLevel(logging.DEBUG)
    logger.debug("FUNC: get_metadata, url: %s, response_type: %s" % (url, response_type))
    sanitized_url = url_utils.sanitize_url(url)
    logger.debug("Sanitized url: %s" % sanitized_url)

    metadata = None
    content_type = None
    response_code = None

    head = url_utils.get_requests_header(sanitized_url)
    if head is None:
        metadata = create_metadata_object(url, StatusCode.BAD_REQUEST, None, None)
        response_code = StatusCode.BAD_REQUEST
        sanitized_url = url
    else:
        sanitized_url = url_utils.get_redirect_url(head)
        content_type = url_utils.get_content_type(head)
        response_code = head.status_code
        metadata = create_metadata_object(url, response_code, sanitized_url, content_type)

    site_response = metadata.fetch_site_data(sanitized_url, response_code)

    # Check for caching, otherwise proceed with scraping
    if config.CACHE_DATA:
        data = cache_utils.get_cached_data(sanitized_url)   # If data from db is None, continue and parse the website
        if data is not None:
            logger.debug("Cache hit for key %s", sanitized_url)
            data_map = json.loads(data.metadata)
            metadata.data_map[FieldKeyword.DATA] = data_map
            return get_json_metadata(metadata.data_map)

    metadata.parse_content(site_response)

    # Trim the description if necessary
    trim_description(metadata, desc_length)

    json_data = get_json_metadata(metadata.data_map)
    logger.info(json_data)
    if config.CACHE_DATA and site_response.status_code == StatusCode.OK:
        cache_map = metadata.get_cache_prop_map()
        cache_data = get_json_metadata(cache_map)
        logger.debug("Caching json data to redis db")
        cache_utils.cache_json_data(sanitized_url, cache_data)
    response = FlaskResponse(response=json_data, status=StatusCode.OK, mimetype="application/json")
    return response


def trim_description(metadata, desc_length):
    if metadata.prop_map['description'] is not None:
        desc = metadata.prop_map['description']
        desc = (desc[:desc_length] + '...') if len(desc) > desc_length else desc
        metadata.prop_map['description'] = desc


def get_json_metadata(map):
    return format_utils.to_json(map)


def create_metadata_object(url, response_code, sanitized_url, content_type):
    logger = current_app.logger
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
    if url_type is UrlTypes.GENERAL:
        return general_metadata.GeneralMetadata(url, response_code, sanitized_url)
    return None

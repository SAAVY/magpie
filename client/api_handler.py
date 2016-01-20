import logging

from flask import current_app
from flask import Response as FlaskResponse

import cache_utils
import config
from constants import ResponseType
from constants import StatusCode
from constants import UrlTypes
import format_utils
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
def get_metadata(url, response_type=ResponseType.JSON):
    logger = current_app.logger
    logger.setLevel(logging.DEBUG)
    logger.debug("FUNC: get_metadata, url: %s, response_type: %s" % (url, response_type))
    sanitized_url = url_utils.sanitize_url(url)
    logger.debug("Sanitized url: %s" % sanitized_url)

    head = url_utils.get_requests_header(sanitized_url)
    if head is None:
        metadata = create_metadata_object(url, StatusCode.BAD_REQUEST, None, None)
    else:
        sanitized_url = url_utils.get_redirect_url(head)
        content_type = url_utils.get_content_type(head)

        metadata = create_metadata_object(url, head.status_code, sanitized_url, content_type)

    if config.CACHE_DATA:
        data = cache_utils.get_cached_data(sanitized_url)   # If data from db is None, continue and parse the website
        if data is not None:
            logger.debug("Cache hit for key %s", sanitized_url)
            return data.metadata
    # return response based on response type
    if response_type == ResponseType.JSON:
        json_data = get_json_metadata(metadata)
        logger.info(json_data)
        if config.CACHE_DATA and head.status_code is StatusCode.OK:
            metadata.get_cache_prop_map()
            cache_data = get_cache_json(metadata)
            logger.debug("Caching json data to redis db")
            cache_utils.cache_json_data(sanitized_url, cache_data)
        response = FlaskResponse(response=json_data, status=StatusCode.OK, mimetype="application/json")
        return response
    return None


def get_json_metadata(metadata):
    return format_utils.to_json(metadata.prop_map)


def get_cache_json(metadata):
    return format_utils.to_json(metadata.cache_map)


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

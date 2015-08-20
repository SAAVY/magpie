import config
import cache_utils
from constants import ResponseType
from constants import UrlTypes
from scraper import drive_metadata
from scraper import dropbox_metadata
from scraper import error_metadata
from scraper import general_metadata
from scraper import wikipedia_metadata
from scraper import youtube_metadata
import url_utils
from utils.profile import cprofile


@cprofile
def get_metadata(url, response_type):
    sanitized_url = url_utils.sanitize_url(url)
    # check response status of website
    head = url_utils.get_requests_header(sanitized_url)
    code = url_utils.get_url_response_code(head)
    if head is None:
        metadata = create_metadata_object(url, code, None)
    else:
        sanitized_url = url_utils.get_redirect_url(head)
    if config.CACHE_DATA:
        data = cache_utils.get_cached_data(sanitized_url)   # If data from db is None, continue and parse the website
        if data is not None:
            return data.metadata
        metadata = create_metadata_object(url, code, sanitized_url)

    # return response based on response type
    if response_type == ResponseType.JSON:
        return get_json_metadata(metadata)


def get_json_metadata(metadata):
    return metadata.to_json()


def create_metadata_object(url, response_code, sanitized_url):
    url_type = url_utils.get_url_type(sanitized_url, response_code)
    if url_type is UrlTypes.ERROR:
        return error_metadata.ErrorMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.DOCS:
        return drive_metadata.DriveMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.DROPBOX:
        return dropbox_metadata.DropboxMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.WIKI:
        return wikipedia_metadata.WikipediaMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.YOUTUBE:
        return youtube_metadata.YoutubeMetadata(url, response_code, sanitized_url)
    if url_type is UrlTypes.GENERAL:
        return general_metadata.GeneralMetadata(url, response_code, sanitized_url)
    return None

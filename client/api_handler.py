from constants import ResponseType
from constants import StatusCode
from constants import UrlTypes
from scraper import drive_metadata
from scraper import error_metadata
from scraper import general_metadata
from scraper import wikipedia_metadata
from scraper import youtube_metadata
import url_utils


def get_metadata(url, response_type):
    validated_response = url_utils.get_url_data(url)
    scraper = get_scraper(validated_response)
    if response_type == ResponseType.JSON:
        return get_json_metadata(scraper)


def get_json_metadata(scraper):
    return scraper.to_json()


def get_scraper(response):
    if response.code != StatusCode.OK:
        return error_metadata.ErrorMetadata(response)
    elif response.type is UrlTypes.DOCS:
        return drive_metadata.DriveMetadata(response)
    elif response.type is UrlTypes.WIKI:
        return wikipedia_metadata.WikipediaMetadata(response)
    elif response.type is UrlTypes.YOUTUBE:
        return youtube_metadata.YoutubeMetadata(response)
    else:
        return general_metadata.GeneralMetadata(response)
    return None

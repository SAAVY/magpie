import json

from bs4 import BeautifulSoup
from flask import current_app

from client.constants import FieldKeyword
from client.constants import MediaTypeValue
from client.constants import MetadataFields
from client.constants import StatusCode
from metadata import Metadata


youtube_request_url = "http://www.youtube.com/oembed?url="


class YoutubeMetadata(Metadata):

    def fetch_site_data(self, sanitized_url, status_code):
        api_url = youtube_request_url + sanitized_url
        response = self.generic_fetch_content(sanitized_url, status_code)

        api_response = self.generic_fetch_content(api_url, status_code)
        if api_response.status_code is StatusCode.OK:
            response.set_api_content(api_response.content)
            response.status_code = api_response.status_code
            response.api_url = api_url

        return response

    def get_json_data(self, response):
        logger = current_app.logger
        if response.api_content is not None:
            try:
                return json.loads(response.api_content)
            except Exception as e:
                logger.exception("JSON EXCEPTION %s" % str(e))
                pass
        return None

    def get_title(self, response):
        data = self.get_json_data(response)
        if data:
            return data["title"]
        return None

    def get_image_list(self, response):
        data = self.get_json_data(response)
        if data:
            images_list = {}
            images_list[FieldKeyword.DATA] = [{
                FieldKeyword.URL: data["thumbnail_url"],
                FieldKeyword.HEIGHT: data["thumbnail_height"],
                FieldKeyword.WIDTH: data["thumbnail_width"]
            }]

            images_list[FieldKeyword.COUNT] = len(images_list[FieldKeyword.DATA])
            return images_list
        return None

    def get_media_list(self, response):
        data = self.get_json_data(response)
        if data:
            media_list = {}
            soup = BeautifulSoup(data["html"], "html.parser")
            iframe = soup.find(MetadataFields.IFRAME)
            embed_url = iframe['src']
            media_list[FieldKeyword.DATA] = [
                {
                    FieldKeyword.URL: embed_url,
                    FieldKeyword.TYPE: MediaTypeValue.VIDEO,
                    FieldKeyword.IFRAME: data["html"]
                }]

            media_list[FieldKeyword.COUNT] = len(media_list[FieldKeyword.DATA])
            return media_list
        return None

    def parse_content(self, response):
        self.generic_parse_content(response)
        self.prop_map[FieldKeyword.API_QUERY_URL] = response.api_url

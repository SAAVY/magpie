import json

from client.constants import FieldKeyword
from client.constants import MediaTypeValue
from metadata import Metadata


youtube_request_url = "http://www.youtube.com/oembed?url="


class YoutubeMetadata(Metadata):

    def fetch_site_data(self, sanitized_url, status_code):
        request_url = youtube_request_url + sanitized_url
        return self.generic_fetch_content(request_url, status_code)

    def parse_content(self, response):
        """
        The youtube metadata parse_content does not call generic_parse_content, since the response is a JSON object
        """
        data = json.loads(response.content)

        self.prop_map[FieldKeyword.TITLE] = data["title"]
        images_list = {}
        images_list[FieldKeyword.DATA] = [
            {
                FieldKeyword.URL: data["thumbnail_url"],
                FieldKeyword.HEIGHT: data["thumbnail_height"],
                FieldKeyword.WIDTH: data["thumbnail_width"]
            }]

        media_list = {}
        media_list[FieldKeyword.DATA] = [
            {
                FieldKeyword.URL: None,
                FieldKeyword.TYPE: MediaTypeValue.VIDEO,
                FieldKeyword.IFRAME: data["html"]
            }]
        images_list[FieldKeyword.COUNT] = len(images_list[FieldKeyword.DATA])
        self.prop_map[FieldKeyword.IMAGES] = images_list

        media_list[FieldKeyword.COUNT] = len(media_list[FieldKeyword.DATA])
        self.prop_map[FieldKeyword.MEDIA] = media_list

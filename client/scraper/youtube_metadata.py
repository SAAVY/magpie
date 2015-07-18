import requests

from client.constants import FieldKeyword
from client.constants import MediaTypeValue
from metadata import Metadata

request_url = "http://www.youtube.com/oembed?url="


class YoutubeMetadata(Metadata):

    def parse_content(self, response):
        self.general_parse_content(response)

        request = request_url + response.url
        resp = requests.get(request)
        data = resp.json()

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

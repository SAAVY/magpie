import requests

from client.constants import FieldKeyword
from client.constants import MediaTypeValue
from metadata import Metadata

request_url = "http://www.youtube.com/oembed?url="


class YoutubeMetadata(Metadata):

    def parse_content(self, response):
        request = request_url + response.url
        resp = requests.get(request)
        data = resp.json()

        self.prop_map[FieldKeyword.URL] = response.url
        self.prop_map[FieldKeyword.SANITIZED_URL] = response.sanitized_url

        self.prop_map[FieldKeyword.TITLE] = data["title"]
        media_list = {}
        media_list[FieldKeyword.DATA] = [
            {
                FieldKeyword.TYPE: MediaTypeValue.IMAGE,
                FieldKeyword.SRC: data["thumbnail_url"]
            },
            {
                FieldKeyword.TYPE: MediaTypeValue.VIDEO,
                FieldKeyword.IFRAME: data["html"]
            }]
        media_list[FieldKeyword.COUNT] = 2
        self.prop_map[FieldKeyword.MEDIA] = media_list

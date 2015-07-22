import json

from bs4 import BeautifulSoup

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

    def parse_content(self, response):
        self.generic_parse_content(response)
        if response.api_content is not None:
            try:
                data = json.loads(response.api_content)

                self.prop_map[FieldKeyword.TITLE] = data["title"]
                images_list = {}
                images_list[FieldKeyword.DATA] = [
                    {
                        FieldKeyword.URL: data["thumbnail_url"],
                        FieldKeyword.HEIGHT: data["thumbnail_height"],
                        FieldKeyword.WIDTH: data["thumbnail_width"]
                    }]

                media_list = {}
                soup = BeautifulSoup(data["html"])
                iframe = soup.find(MetadataFields.IFRAME)
                embed_url = iframe['src']
                media_list[FieldKeyword.DATA] = [
                    {
                        FieldKeyword.URL: embed_url,
                        FieldKeyword.TYPE: MediaTypeValue.VIDEO,
                        FieldKeyword.IFRAME: data["html"]
                    }]
                images_list[FieldKeyword.COUNT] = len(images_list[FieldKeyword.DATA])
                self.prop_map[FieldKeyword.IMAGES] = images_list
                self.prop_map[FieldKeyword.API_QUERY_URL] = response.api_url

                media_list[FieldKeyword.COUNT] = len(media_list[FieldKeyword.DATA])
                self.prop_map[FieldKeyword.MEDIA] = media_list
            except Exception:
                # TODO: log exception in reading json response
                pass

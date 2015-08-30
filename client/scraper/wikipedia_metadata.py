from wikipedia import DisambiguationError

from urlparse import urlparse
import collections
import json
import re
import requests

from client.constants import FieldKeyword
from metadata import Metadata


class WikipediaMetadata(Metadata):

    def build_fetch_data_url(self, title):
        base_api_url = "https://en.wikipedia.org/w/api.php?"
        query = collections.OrderedDict([
            ("action", "query"),
            ("prop", "imageinfo%7Cinfo%7Cpageimages"),
            ("format", "json"),
            ("iiprop", "url"),
            ("inprop", "readable"),
            ("piprop", "thumbnail"),
            ("pithumbsize", "500"),
            ("exintro", ""),
            ("titles", title)
        ])
        api_url = base_api_url
        api_url += "&".join("%s=%s" % (key, val) for (key, val) in query.iteritems())
        return api_url

    def get_desc(self, response):
        page = response.wiki_page
        if page is not None and page.summary is not None:
            return page.summary
        return None

    def get_images_list(self, response):
        page = response.wiki_page
        if page is not None and page.images is not None:
            images_list = {}
            img_count = 10 if len(page.images) > 9 else len(page.images)
            images_list[FieldKeyword.COUNT] = img_count
            data = []
            for image in page.images[:img_count]:
                image_item = collections.OrderedDict()
                image_item[FieldKeyword.URL] = image
                data.append(image_item)

            images_list[FieldKeyword.DATA] = data
            return images_list
        return None

    def fetch_site_data(self, sanitized_url, status_code):
        response = self.generic_fetch_content(sanitized_url, status_code)
        parsed_url = urlparse(sanitized_url)
        path = re.search(r"wiki\/(\S+)", parsed_url.path)
        page = None

        if path is not None:
            title = path.group(1)
            try:
                web_request = requests.get(self.build_fetch_data_url(title))
                json_data = json.loads(web_request.content)
                page = json_data["query"]["pages"]

            except DisambiguationError as error:
                print error
                # TODO: do something when there's a disambiguation error
                error

        response.set_wiki_content(page)
        return response

    def parse_content(self, response):
        self.generic_parse_content(response)

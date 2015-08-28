from bs4 import BeautifulSoup
import collections
import json
import re
import requests
from urlparse import urlparse

from wikipedia import DisambiguationError

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
                # TODO: do something when there's a disambiguation error
                error

        response.set_wiki_content(page)
        return response

    def parse_content(self, response):
        self.generic_parse_content(response)

        keys = response.wiki_page.keys()
        page = response.wiki_page[keys[0]]

        if page is not None and "extract" in page:
            self.prop_map[FieldKeyword.DESC] = BeautifulSoup(page["extract"]).text

        if page is not None and "thumbnail" in page:
            images_list = {}
            images_list[FieldKeyword.COUNT] = 1
            image_data = []
            image_item = collections.OrderedDict()
            if page["thumbnail"]["source"]:
                image_item[FieldKeyword.URL] = page["thumbnail"]["source"]
            if page["thumbnail"]["width"]:
                image_item[FieldKeyword.WIDTH] = page["thumbnail"]["width"]
            if page["thumbnail"]["width"]:
                image_item[FieldKeyword.HEIGHT] = page["thumbnail"]["height"]
            image_data.append(image_item)

            images_list[FieldKeyword.DATA] = image_data
            self.prop_map[FieldKeyword.IMAGES] = images_list

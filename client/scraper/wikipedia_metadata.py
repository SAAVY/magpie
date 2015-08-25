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

    fetch_data_url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts%7Cimageinfo%7Cinfo%7Cpageimages&format=json&exchars=2000&iiprop=url&inprop=readable&piprop=thumbnail%7Cname&exintro=&titles="

    def fetch_site_data(self, sanitized_url, status_code):
        response = self.generic_fetch_content(sanitized_url, status_code)
        parsed_url = urlparse(sanitized_url)
        path = re.search(r"wiki\/(\S+)", parsed_url.path)
        page = None

        if path is not None:
            title = path.group(1)
            try:
                web_request = requests.get(self.fetch_data_url + title)
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
            data = []
            image_item = collections.OrderedDict()
            image_item[FieldKeyword.URL] = page["thumbnail"]["source"]
            data.append(image_item)

            images_list[FieldKeyword.DATA] = data
            self.prop_map[FieldKeyword.IMAGES] = images_list

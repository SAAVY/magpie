import collections
import re
from urlparse import urlparse

import wikipedia
from wikipedia import DisambiguationError

from client.constants import FieldKeyword
from metadata import Metadata


class WikipediaMetadata(Metadata):

    def fetch_site_data(self, sanitized_url, status_code):
        response = self.generic_fetch_content(sanitized_url, status_code)
        parsed_url = urlparse(sanitized_url)
        path = re.search(r"wiki\/(\S+)", parsed_url.path)
        page = None

        if path is not None:
            title = path.group(1)
            try:
                page = wikipedia.page(title)
            except DisambiguationError as error:
                # TODO: do something when there's a disambiguation error
                error

        response.set_wiki_content(page)
        return response

    def parse_content(self, response):
        self.generic_parse_content(response)

        page = response.wiki_page

        if page is not None and page.summary is not None:
            self.prop_map[FieldKeyword.DESC] = page.summary

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
            self.prop_map[FieldKeyword.IMAGES] = images_list

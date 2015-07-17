import collections
import re

import lxml.html
import wikipedia

from client.constants import FieldKeyword
from metadata import Metadata


class WikipediaMetadata(Metadata):

    def parse_content(self, response):
        self.general_parse_content(response)

        m = re.search(r"wiki\/(\S+)", response.url)
        title = m.group(1)
        document = lxml.html.fromstring(response.content)

        page = wikipedia.page(title)
        self.prop_map[FieldKeyword.DESC] = page.summary
        self.prop_map[FieldKeyword.TITLE] = document.find(".//title").text
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

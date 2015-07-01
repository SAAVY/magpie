import re

import lxml.html
import wikipedia

from client.constants import FieldKeyword
from client.constants import FieldValue
from metadata import Metadata


class WikipediaMetadata(Metadata):

    def parse_content(self, response):
        m = re.search(r"wiki\/(\S+)", response.url)
        title = m.group(1)
        document = lxml.html.fromstring(response.content)

        self.prop_map[FieldKeyword.URL] = response.url
        self.prop_map[FieldKeyword.SANITIZED_URL] = response.sanitized_url

        page = wikipedia.page(title)
        self.prop_map[FieldKeyword.DESC] = page.summary
        self.prop_map[FieldKeyword.TITLE] = document.find(".//title").text
        media_list = {}
        img_count = 10 if len(page.images) > 9 else len(page.images)
        media_list[FieldKeyword.COUNT] = img_count
        data = []
        for image in page.images[:img_count]:
            media_item = {}
            media_item[FieldKeyword.TYPE] = FieldValue.IMAGE
            media_item[FieldKeyword.SRC] = image
            data.append(media_item)

        media_list[FieldKeyword.DATA] = data
        self.prop_map[FieldKeyword.MEDIA] = media_list

from bs4 import BeautifulSoup

import collections
import json

from flask import Response

from client.constants import FieldKeyword
from client.constants import MediaTypeValue
from client.constants import MetadataFields
from client.constants import StatusCode


class Metadata:

    def __init__(self, response):
        self.prop_map = collections.OrderedDict()
        self.prop_map[FieldKeyword.STATUS] = response.code
        self.prop_map[FieldKeyword.URL] = response.url
        self.prop_map[FieldKeyword.SANITIZED_URL] = response.sanitized_url
        self.parse_content(response)

    def parse_content(self, response):
        raise NotImplementedError("Every metadata scraper must implement parse_content")

    def to_json(self):
        json_data = json.dumps(self.prop_map)
        response = Response(response=json_data, status=StatusCode.OK, mimetype="application/json")
        return response

    def get_title(self, soup):
        title = soup.findAll(attrs={MetadataFields.PROPERTY: MetadataFields.OG_TITLE})
        if len(title) == 0:
            title = soup.findAll(attrs={MetadataFields.NAME: MetadataFields.TITLE})
        if len(title) == 0:
            title = soup.html.head.title
            if not title:
                return ""
            return soup.html.head.title.string
        return title[0]['content'].encode('utf-8')

    def get_desc(self, soup):
        desc = soup.findAll(attrs={MetadataFields.PROPERTY: MetadataFields.OG_DESC})
        if len(desc) == 0:
            desc = soup.findAll(attrs={MetadataFields.NAME: MetadataFields.DESCRIPTION})
        if len(desc) == 0:
            return ""
        return desc[0]['content'].encode('utf-8')

    def get_image_url(self, soup):
        image_url = soup.findAll(attrs={MetadataFields.PROPERTY: MetadataFields.OG_IMAGE})
        if len(image_url) == 0:
            return ""
        return image_url[0]['content'].encode('utf-8')

    def general_parse_content(self, response):
        soup = BeautifulSoup(response.content)
        title = self.get_title(soup)
        desc = self.get_desc(soup)
        image_url = self.get_image_url(soup)

        if title:
            self.prop_map[FieldKeyword.TITLE] = title

        if desc:
            self.prop_map[FieldKeyword.DESC] = desc

        if image_url:
            media_list = collections.OrderedDict()
            media_list[FieldKeyword.COUNT] = 1
            media_list[FieldKeyword.DATA] = []
            data = {
                FieldKeyword.URL: image_url,
                FieldKeyword.TYPE: MediaTypeValue.IMAGE
            }
            media_list[FieldKeyword.DATA].append(data)
            self.prop_map[FieldKeyword.MEDIA] = media_list

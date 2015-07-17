import collections
import json

from bs4 import BeautifulSoup
from flask import Response

from client.constants import FieldKeyword
from client.constants import MetadataFields
from client.constants import StatusCode


class Metadata:

    def __init__(self, response):
        self.prop_map = collections.OrderedDict()
        self.prop_map[FieldKeyword.STATUS] = response.code
        self.prop_map[FieldKeyword.URL] = response.sanitized_url
        self.prop_map[FieldKeyword.REQUEST_URL] = response.url
        self.prop_map[FieldKeyword.DOMAIN_URL] = response.domain_url
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
                return None
            return soup.html.head.title.string
        return title[0]['content'].encode('utf-8')

    def get_desc(self, soup):
        desc = soup.findAll(attrs={MetadataFields.PROPERTY: MetadataFields.OG_DESC})
        if len(desc) == 0:
            desc = soup.findAll(attrs={MetadataFields.NAME: MetadataFields.DESCRIPTION})
        if len(desc) == 0:
            return None
        return desc[0]['content'].encode('utf-8')

    def get_images_list(self, soup):
        images_list = collections.OrderedDict()
        image_urls = soup.findAll(attrs={MetadataFields.PROPERTY: MetadataFields.OG_IMAGE})
        if len(image_urls) == 0:
            return None
        images_list[FieldKeyword.COUNT] = len(image_urls)
        images_list[FieldKeyword.DATA] = []
        for i in range(len(image_urls)):
            image_item_dict = collections.OrderedDict()
            image_item_dict[FieldKeyword.URL] = image_urls[i]['content'].encode('utf-8')
            images_list[FieldKeyword.DATA].append(image_item_dict)

        return images_list

    def get_favicon_url(self, soup):
        icon_link = None
        icon_field = soup.find(MetadataFields.LINK, attrs={MetadataFields.REL: "icon", "type": "image/x-icon"})
        if not icon_field:
            icon_field = soup.find(MetadataFields.LINK, attrs={MetadataFields.REL: "icon"})
        if icon_field:
            icon_link = icon_field['href'].encode('utf-8')
        return icon_link

    def general_parse_content(self, response):
        soup = BeautifulSoup(response.content)
        title = self.get_title(soup)
        desc = self.get_desc(soup)
        images_list = self.get_images_list(soup)
        favicon_url = self.get_favicon_url(soup)

        self.prop_map[FieldKeyword.TITLE] = title

        self.prop_map[FieldKeyword.DESC] = desc

        self.prop_map[FieldKeyword.FAVICON] = favicon_url

        self.prop_map[FieldKeyword.IMAGES] = images_list

        self.prop_map[FieldKeyword.MEDIA] = None

        self.prop_map[FieldKeyword.FILES] = None

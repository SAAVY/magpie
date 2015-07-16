from bs4 import BeautifulSoup

from client.constants import FieldKeyword
from client.constants import FieldValue
from client.constants import MetadataFields
from metadata import Metadata


class GeneralMetadata(Metadata):

    def parse_content(self, response):
        soup = BeautifulSoup(response.content)
        title = self.get_title(soup)
        desc = self.get_desc(soup)
        image_url = self.get_image_url(soup)

        if title:
            self.prop_map[FieldKeyword.TITLE] = title

        if desc:
            self.prop_map[FieldKeyword.DESC] = desc

        if image_url:
            media_list = {}
            media_list[FieldKeyword.COUNT] = 1
            media_list[FieldKeyword.DATA] = []
            data = {
                FieldKeyword.TYPE: FieldValue.IMAGE,
                FieldKeyword.SRC: image_url
            }
            media_list[FieldKeyword.DATA].append(data)
            self.prop_map[FieldKeyword.MEDIA] = media_list

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

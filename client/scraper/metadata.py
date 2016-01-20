from bs4 import BeautifulSoup

import collections
import requests

from client import url_utils
from client.constants import FieldKeyword
from client.constants import MetadataFields
from client.response import Response


class Metadata:

    def __init__(self, url, response_code, sanitized_url):
        self.prop_map = collections.OrderedDict()
        self.cache_map = collections.OrderedDict()
        self.init_fields()
        self.prop_map[FieldKeyword.REQUEST_URL] = url
        self.prop_map[FieldKeyword.URL] = sanitized_url
        response = self.fetch_site_data(sanitized_url, response_code)
        self.prop_map[FieldKeyword.STATUS] = response_code
        self.prop_map[FieldKeyword.PROVIDER_URL] = response.provider_url
        self.parse_content(response)

    def init_fields(self):
        self.prop_map[FieldKeyword.STATUS] = None
        self.prop_map[FieldKeyword.ERROR_MSG] = None
        self.prop_map[FieldKeyword.URL] = None
        self.prop_map[FieldKeyword.REQUEST_URL] = None
        self.prop_map[FieldKeyword.PROVIDER_URL] = None
        self.prop_map[FieldKeyword.API_QUERY_URL] = None
        self.prop_map[FieldKeyword.TITLE] = None
        self.prop_map[FieldKeyword.DESC] = None
        self.prop_map[FieldKeyword.FAVICON] = None
        self.prop_map[FieldKeyword.IMAGES] = None
        self.prop_map[FieldKeyword.MEDIA] = None
        self.prop_map[FieldKeyword.FILES] = None

    def fetch_site_data(self, sanitized_url, status_code):
        """
        fetch_site_data makes a http request to website stated to get website content.
        This method should be the only method that makes network calls.

        You may call generic_fetch_content to help with initial fetch of data

        Args:
            url: The sanitized request url
            status_code: The HTTP reponse code of the site
        Returns:
            a Response object with the data
        Raises:
            NotImplementedError if subclasses does not implement method
        """
        raise NotImplementedError("Every metadata scraper must implement fetch_site_data")

    def parse_content(self, response):
        """
        parse_content makes a http request to website stated to get website content.
        This method should be the only method that makes network calls.

        You may call generic_parse_content to help with initial parsing of data

        Args:
            response: The unsanitized request url
        Returns:
            None
        Raises:
            NotImplementedError if subclasses does not implement method
        """
        raise NotImplementedError("Every metadata scraper must implement parse_content")

    def get_cache_prop_map(self):
        self.cache_map[FieldKeyword.URL] = self.prop_map[FieldKeyword.URL]
        self.cache_map[FieldKeyword.TITLE] = self.prop_map[FieldKeyword.TITLE]
        self.cache_map[FieldKeyword.DESC] = self.prop_map[FieldKeyword.DESC]
        self.cache_map[FieldKeyword.FAVICON] = self.prop_map[FieldKeyword.FAVICON]
        self.cache_map[FieldKeyword.IMAGES] = self.prop_map[FieldKeyword.IMAGES]
        self.cache_map[FieldKeyword.MEDIA] = self.prop_map[FieldKeyword.MEDIA]
        self.cache_map[FieldKeyword.FILES] = self.prop_map[FieldKeyword.FILES]
        return self.cache_map

    def get_title(self, soup):
        title_html = soup.findAll(MetadataFields.META, attrs={MetadataFields.PROPERTY: MetadataFields.OG_TITLE})
        title = None
        if len(title_html) == 0:
            title_html = soup.findAll(MetadataFields.META, attrs={MetadataFields.NAME: MetadataFields.TITLE})
        if len(title_html) == 0:
            if soup.html.head and soup.html.head.title:
                title = soup.html.head.title.string
        for i in range(len(title_html)):
            if title_html[i].has_attr('content'):
                title = title_html[i]['content'].encode('utf-8')
                break
        return title

    def get_desc(self, soup):
        desc_html = soup.findAll(MetadataFields.META, attrs={MetadataFields.PROPERTY: MetadataFields.OG_DESC})
        desc = None
        if len(desc_html) == 0:
            desc_html = soup.findAll(MetadataFields.META, attrs={MetadataFields.NAME: MetadataFields.DESCRIPTION})
            if len(desc_html) == 0:
                desc = None
        for i in range(len(desc_html)):
            if desc_html[i].has_attr('content'):
                desc = desc_html[i]['content'].encode('utf-8')
                break
        return desc

    def get_images_list(self, soup):
        images_list = collections.OrderedDict()
        image_urls = soup.findAll(MetadataFields.META, attrs={MetadataFields.PROPERTY: MetadataFields.OG_IMAGE})
        if len(image_urls) == 0:
            return None
        images_list[FieldKeyword.COUNT] = 0
        images_list[FieldKeyword.DATA] = []
        for i in range(len(image_urls)):
            image_item_dict = collections.OrderedDict()
            if image_urls[i].has_attr('content'):
                image_item_dict[FieldKeyword.URL] = image_urls[i]['content'].encode('utf-8')
                images_list[FieldKeyword.DATA].append(image_item_dict)
                images_list[FieldKeyword.COUNT] = images_list[FieldKeyword.COUNT] + 1
        if images_list[FieldKeyword.COUNT] > 0:
            return images_list
        return None

    def get_favicon_url(self, soup):
        icon_link = None
        icon_field = soup.find(MetadataFields.LINK, attrs={MetadataFields.REL: "icon", MetadataFields.TYPE: "image/x-icon"})
        if not icon_field:
            icon_field = soup.find(MetadataFields.LINK, attrs={MetadataFields.REL: "icon"})
        if icon_field:
            icon_link = icon_field['href'].encode('utf-8')

        provider_url = self.prop_map[FieldKeyword.PROVIDER_URL]
        if icon_link:
            icon_link = url_utils.validate_image_url(icon_link, provider_url)

        return icon_link

    def generic_fetch_content(self, request_url, status_code):
        response = Response()

        request = requests.get(request_url)
        redirect_url = request.url

        provider_url = url_utils.get_domain_url(redirect_url)
        response.set_content(request.headers, request.content, request.status_code, redirect_url, request_url, provider_url)
        return response

    def generic_parse_content(self, response):
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

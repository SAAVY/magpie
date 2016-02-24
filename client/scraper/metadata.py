from bs4 import BeautifulSoup

import collections
from flask import current_app
import requests

from client import config
from client import url_utils
from client.constants import FieldKeyword
from client.constants import MetadataFields
from client.response import Response


class Metadata:

    def __init__(self, request_url, response_code, sanitized_url):

        self.prop_map = collections.OrderedDict()
        self.data_map = collections.OrderedDict()
        self.init_fields()

        self.data_map[FieldKeyword.REQUEST_URL] = request_url
        self.data_map[FieldKeyword.STATUS] = response_code
        self.data_map[FieldKeyword.DATA] = self.prop_map

        self.prop_map[FieldKeyword.URL] = sanitized_url

    def init_fields(self):
        self.data_map[FieldKeyword.STATUS] = None
        self.data_map[FieldKeyword.ERROR_MSG] = None
        self.data_map[FieldKeyword.REQUEST_URL] = None
        self.data_map[FieldKeyword.DATA] = None

        self.prop_map[FieldKeyword.URL] = None
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
        return self.prop_map

    def get_title(self, response):
        soup = BeautifulSoup(response.content)
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

    def get_desc(self, response):
        soup = BeautifulSoup(response.content)
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

    def get_images_list(self, response):
        soup = BeautifulSoup(response.content)
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

    def get_favicon_url(self, response):
        soup = BeautifulSoup(response.content)
        icon_link = None
        icon_field = soup.find(MetadataFields.LINK, attrs={MetadataFields.REL: "icon", MetadataFields.TYPE: "image/x-icon"})
        if icon_field:
            icon_link = icon_field['href'].encode('utf-8')
        else:
            icon_field = soup.find(MetadataFields.LINK, attrs={MetadataFields.REL: "icon"})
        if icon_link:
            icon_link = url_utils.validate_image_url(icon_link, self.prop_map[FieldKeyword.PROVIDER_URL])
        return icon_link

    def get_media_list(self, response):
        return None

    def get_files_list(self, response):
        return None

    def generic_fetch_content(self, request_url, status_code):
        logger = current_app.logger
        logger.debug("generic_fetch_content, request_url: %s status_code: %d" % (request_url, status_code))
        response = Response()

        request = requests.get(request_url)
        redirect_url = request.url

        provider_url = url_utils.get_domain_url(redirect_url)
        response.set_content(request.headers, request.content, request.status_code, redirect_url, request_url, provider_url)
        if not config.CACHE_DATA:
            self.data_map[FieldKeyword.STATUS] = response.status_code
            self.prop_map[FieldKeyword.PROVIDER_URL] = response.provider_url
        else:
            self.data_map[FieldKeyword.STATUS] = status_code
            self.prop_map[FieldKeyword.PROVIDER_URL] = provider_url
        return response

    def generic_parse_content(self, response):
        logger = current_app.logger
        try:
            self.prop_map[FieldKeyword.TITLE] = self.get_title(response)

            self.prop_map[FieldKeyword.DESC] = self.get_desc(response)

            self.prop_map[FieldKeyword.IMAGES] = self.get_images_list(response)

            self.prop_map[FieldKeyword.FAVICON] = self.get_favicon_url(response)

            self.prop_map[FieldKeyword.MEDIA] = self.get_media_list(response)

            self.prop_map[FieldKeyword.FILES] = self.get_files_list(response)

        except KeyError as e:
            logger.exception("generic_parse_content KeyError Exception: %s" % str(e))
        except Exception as e:
            logger.exception("generic_parse_content Exception: %s" % str(e))

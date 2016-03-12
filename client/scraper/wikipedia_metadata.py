from wikipedia import DisambiguationError

from urlparse import urlparse
import collections
from flask import current_app
import json
import re

from client.constants import FieldKeyword
from metadata import Metadata
from client import url_utils


class WikipediaMetadata(Metadata):

    def build_fetch_data_url(self, title):
        base_api_url = "https://en.wikipedia.org/w/api.php?"
        query = collections.OrderedDict([
            ("action", "query"),
            ("prop", "extracts|imageinfo|pageimages|videoinfo"),
            ("iiprop", "url"),
            ("exlimit", "1"),
            ("exintro", ""),
            ("explaintext", ""),
            ("format", "json"),
            ("piprop", "thumbnail%7Cname%7Coriginal"),
            ("viprop", "canonicaltitle%7Curl"),
            ("titles", title)
        ])
        api_url = base_api_url
        api_url += "&".join("%s=%s" % (key, val) for (key, val) in query.iteritems())
        print api_url
        return api_url

    def get_desc(self, response):
        page = response.wiki_page
        if page is not None and FieldKeyword.EXTRACT in page:
            return page[FieldKeyword.EXTRACT]
        return None

    def get_images_list(self, response):
        page = response.wiki_page
        if page is not None and FieldKeyword.THUMBNAIL in page and page[FieldKeyword.THUMBNAIL]:
            images_list = {}
            images_list[FieldKeyword.COUNT] = 1
            image_data = []
            image_item = collections.OrderedDict()
            if page[FieldKeyword.THUMBNAIL][FieldKeyword.SOURCE]:
                image_item[FieldKeyword.URL] = page[FieldKeyword.THUMBNAIL][FieldKeyword.SOURCE]
            if page[FieldKeyword.THUMBNAIL][FieldKeyword.WIDTH]:
                image_item[FieldKeyword.WIDTH] = page[FieldKeyword.THUMBNAIL][FieldKeyword.WIDTH]
            if page[FieldKeyword.THUMBNAIL][FieldKeyword.HEIGHT]:
                image_item[FieldKeyword.HEIGHT] = page[FieldKeyword.THUMBNAIL][FieldKeyword.HEIGHT]
            image_data.append(image_item)
            print page[FieldKeyword.THUMBNAIL]

            images_list[FieldKeyword.DATA] = image_data
            return images_list
        return None

    def fetch_site_data(self, sanitized_url, status_code):
        logger = current_app.logger
        response = self.generic_fetch_content(sanitized_url, status_code)
        parsed_url = urlparse(sanitized_url)
        path = re.search(r"wiki\/(\S+)", parsed_url.path)
        page = None

        if path is not None:
            title = path.group(1)
            try:
                web_request = url_utils.get_requests_content(self.build_fetch_data_url(title))
                json_data = json.loads(web_request.content)
                if "warnings" in json_data and json_data["warnings"]:
                    print "WARNING: Error with wikipedia query: ", json_data["warnings"]['main']
                for p in json_data["query"]["pages"]:
                    page = json_data["query"]["pages"][p]
            except DisambiguationError as error:
                logger.exception("DisambiguationError: %s", str(error))

        response.set_wiki_content(page)
        return response

    def parse_content(self, response):
        self.generic_parse_content(response)

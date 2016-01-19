import unittest
import mock
from client.response import Response
from client.constants import UrlTypes
from client.scraper.wikipedia_metadata import WikipediaMetadata


class TestWikipediaMetadata(unittest.TestCase):

    wikipedia_url = "https://en.wikipedia.org/wiki/Starbucks"

    @mock.patch.object(WikipediaMetadata, 'generic_fetch_content')
    def test_wikipedia_metadata(self, content):
        with open("test/mocks/wikipedia.html", "r") as testFile:
            data = testFile.read()

        response = Response()
        response.set_content("", data, "", self.wikipedia_url, self.wikipedia_url, UrlTypes.WIKI)

        content.return_value = response

        scraper = WikipediaMetadata(self.wikipedia_url, 200, self.wikipedia_url)

        scraped_response = scraper.prop_map
        self.assertTrue(scraped_response['images']['data'][0]['url'] is not None)
        self.assertTrue(scraped_response['images']['count'] is 1)
        self.assertTrue(scraped_response['title'] is not None)
        self.assertTrue(scraped_response['images'] is not None)
        self.assertEqual(scraped_response.get("status"), 200)

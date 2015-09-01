import unittest
import mock

from client.scraper.youtube_metadata import YoutubeMetadata
from client.response import Response
from client.constants import FieldKeyword
from client.constants import MediaTypeValue
from client.constants import StatusCode
from client.constants import UrlTypes

test_url = "https://www.youtube.com/watch?v=_UfFY6PSVu0"


class TestYoutubeMetadata(unittest.TestCase):

    def patch_fetch_content(*args, **kwargs):
        with open("test/mocks/youtube.json", "r") as testFile:
            data = testFile.read()

        response = Response()
        response.set_content("", data, 200, test_url, test_url, UrlTypes.YOUTUBE)
        return response

    @mock.patch('client.scraper.metadata.Metadata.generic_fetch_content', side_effect=patch_fetch_content)
    def test_youtube(self, fetch_site_data):

        scraper = YoutubeMetadata(test_url, 200, test_url)

        scraped_response = scraper.prop_map
        self.assertTrue(scraped_response[FieldKeyword.MEDIA][FieldKeyword.DATA][0][FieldKeyword.HTML] is not None)
        self.assertTrue(scraped_response[FieldKeyword.MEDIA][FieldKeyword.DATA][0][FieldKeyword.TYPE] is MediaTypeValue.VIDEO)
        self.assertTrue(scraped_response[FieldKeyword.TITLE] is not None)
        self.assertTrue(scraped_response[FieldKeyword.IMAGES] is not None)
        self.assertEqual(scraped_response[FieldKeyword.STATUS], StatusCode.OK)

if __name__ == '__main__':
    unittest.main()

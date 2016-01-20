import unittest
# import mock
import json

# from client.scraper.youtube_metadata import YoutubeMetadata
from client.response import Response
# from client.constants import FieldKeyword
# from client.constants import MediaTypeValue
# from client.constants import StatusCode
from client.constants import UrlTypes

test_url = "https://www.youtube.com/watch?v=_UfFY6PSVu0"


class TestYoutubeMetadata(unittest.TestCase):

    def get_json_data(self, response):
        with open("test/mocks/youtube.json", "r") as testFile:
            data = testFile.read()
        return json.loads(data)

    def patch_fetch_content(*args, **kwargs):
        with open("test/mocks/youtube.json", "r") as testFile:
            data = testFile.read()

        response = Response()
        response.set_content("", "", 200, test_url, test_url, UrlTypes.YOUTUBE)
        response.set_api_content(data)
        return response

    def test_youtube(self):
        pass

        # scraper = YoutubeMetadata(test_url, 200, test_url)

        # scraped_response = scraper.prop_map
        # self.assertTrue(scraped_response[FieldKeyword.MEDIA][FieldKeyword.DATA][0][FieldKeyword.HTML] is not None)
        # self.assertTrue(scraped_response[FieldKeyword.MEDIA][FieldKeyword.DATA][0][FieldKeyword.TYPE] is MediaTypeValue.VIDEO)
        # self.assertTrue(scraped_response[FieldKeyword.TITLE] is not None)
        # self.assertTrue(scraped_response[FieldKeyword.IMAGES] is not None)
        # self.assertEqual(scraped_response[FieldKeyword.STATUS], StatusCode.OK)
        # TODO: update unit tests

if __name__ == '__main__':
    unittest.main()

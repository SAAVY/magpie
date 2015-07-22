import unittest
from client.scraper.youtube_metadata import YoutubeMetadata
from client.response import Response
from client.constants import UrlTypes

test_url = "https://www.youtube.com/watch?v=_UfFY6PSVu0"


class TestYoutubeMetadata(unittest.TestCase):

    def test_youtube(self):
        with open("test/mocks/youtube.json", "r") as testFile:
            data = testFile.read()

        response = Response()
        response.set_content("", data, "", test_url, UrlTypes.get_special_url(UrlTypes.YOUTUBE))

        scraper = YoutubeMetadata(test_url, 200, test_url)

        scraped_response = scraper.prop_map
        self.assertTrue(scraped_response['media']['data'][0]['iframe'] is not None)
        self.assertTrue(scraped_response['media']['data'][0]['type'] is 'video')
        self.assertTrue(scraped_response['title'] is not None)
        self.assertTrue(scraped_response['images'] is not None)
        self.assertEqual(scraped_response.get("status"), 200)

if __name__ == '__main__':
    unittest.main()

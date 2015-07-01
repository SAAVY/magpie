import unittest
from client.api import app
import json


class TestWikipediaMetadata(unittest.TestCase):

    wikipedia_url = "https://en.wikipedia.org/wiki/University_of_Waterloo"

    def test_wikipedia_metadata(self):
        tester = app.test_client(self)
        response = tester.get('/website?src=' + self.wikipedia_url)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("title"), "University of Waterloo - Wikipedia, the free encyclopedia")

if __name__ == '__main__':
    unittest.main()

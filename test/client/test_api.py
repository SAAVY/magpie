import unittest
import json

from client.api import app
from client.query_utils import QueryParams
from client.constants import ResponseType
import client.api
import client.api_handler


class TestApi(unittest.TestCase):

    url1 = "https://github.com"
    url2 = "https://www.youtube.com/watch?v=_UfFY6PSVu0"

    def test_root_page(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_multiple_request(self):
        query_param = QueryParams()
        query_param.query_urls = [self.url1, self.url2]
        query_param.desc_length = 500
        query_param.response_type = ResponseType.JSON

        with client.api.app.app_context():
            response = client.api_handler.get_urls_metadata(query_param)
            json_str = response.response[0]
            json_response = json.loads(json_str)

            self.assertTrue(json_response['response_count'] == 2)
            self.assertTrue(len(json_response['responses']) == 2)

            for response in json_response['responses']:
                self.assertTrue(response['data']['title'] is not None)
                self.assertTrue(response['data']['description'] is not None)
                self.assertTrue(response['data']['favicon'] is not None)
                self.assertTrue(response['data']['images']['count'] > 0)
                self.assertEqual(response['status'], 200)

if __name__ == '__main__':
    unittest.main()

import unittest
import json
from client.query_utils import QueryParams
from client.constants import ResponseType
import client.api_handler
import client.api


class TestImageUrlMetadata(unittest.TestCase):

    test_url = "https://goo.gl/x6ZKLz"

    def test_image(self):

        query_param = QueryParams()
        query_param.query_urls = [self.test_url]
        query_param.desc_length = 500
        query_param.response_type = ResponseType.JSON

        with client.api.app.app_context():
            response = client.api_handler.get_url_metadata(query_param)
            json_str = response.response[0]
            json_response = json.loads(json_str)

            self.assertTrue(json_response['data']['title'] is not None)
            self.assertTrue(json_response['data']['images']['count'] > 0)
            self.assertEqual(json_response['status'], 200)


if __name__ == '__main__':
    unittest.main()

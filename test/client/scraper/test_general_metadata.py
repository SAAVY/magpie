import unittest
import json
from client.query_utils import QueryParams
from client.constants import ResponseType
import client.api_handler
import client.api


class TestGeneralMetadata(unittest.TestCase):

    test_urls = ["https://github.com",
                 "https://www.instagram.com/p/BCowGiICmTk/",
                 "http://www.yelp.com/biz/greenhearts-family-farm-csa-san-francisco"]

    def test_general(self):

        query_param = QueryParams()
        for test_url in self.test_urls:
            query_param.query_urls = [test_url]
            query_param.desc_length = 500
            query_param.response_type = ResponseType.JSON

            with client.api.app.app_context():
                response = client.api_handler.get_url_metadata(query_param)
                json_str = response.response[0]
                json_response = json.loads(json_str)

                self.assertTrue(json_response['data']['title'] is not None)
                self.assertTrue(json_response['data']['description'] is not None)
                self.assertTrue(json_response['data']['favicon'] is not None)
                self.assertTrue(json_response['data']['images']['count'] > 0)
                self.assertEqual(json_response['status'], 200)

if __name__ == '__main__':
    unittest.main()

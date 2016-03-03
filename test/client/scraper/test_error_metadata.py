import unittest
import json
from client.query_utils import QueryParams
from client.constants import ResponseType
import client.api_handler
import client.api


class TestErrorMetadata(unittest.TestCase):

    test_url = "https://github.com/invalidurl"

    def test_error(self):

        query_param = QueryParams()
        query_param.query_urls = [self.test_url]
        query_param.desc_length = 500
        query_param.response_type = ResponseType.JSON

        with client.api.app.app_context():
            response = client.api_handler.get_url_metadata(query_param)
            json_str = response.response[0]
            json_response = json.loads(json_str)

            self.assertEqual(json_response['status'], 404)
            self.assertTrue(json_response['error_message'] is not None)


if __name__ == '__main__':
    unittest.main()

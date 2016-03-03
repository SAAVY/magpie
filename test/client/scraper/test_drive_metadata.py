import unittest
import json
from client.query_utils import QueryParams
from client.constants import ResponseType
import client.api_handler
import client.api


class TestDriveMetadata(unittest.TestCase):

    test_public_url = "https://docs.google.com/document/d/1tPzlb1PmLgRWwePwxH4OXsp5UrKHa4BZMl0ho4sM8Sk/edit?usp=sharing"
    test_private_url = "https://docs.google.com/document/d/1xGtyzzZv4NxcxFQNUC59ckgI_viRRQNh77tGfh8yxt0/edit"
    test_invalid_url = "https://docs.google.com/document/d/invalidurl"

    def test_drive(self, url=""):

        query_param = QueryParams()
        query_param.query_urls = [url]
        query_param.desc_length = 500
        query_param.response_type = ResponseType.JSON

        with client.api.app.app_context():
            response = client.api_handler.get_url_metadata(query_param)
            json_str = response.response[0]
            json_response = json.loads(json_str)
            return json_response

        return None

    def test_public_drive(self):
        json_response = self.test_drive(self.test_public_url)

        self.assertTrue(json_response['data']['title'] is not None)
        self.assertTrue(json_response['data']['description'] is not None)
        self.assertTrue(json_response['data']['images']['count'] > 0)
        self.assertTrue(json_response['data']['files']['count'] > 0)
        self.assertEqual(json_response['status'], 200)

    def test_private_drive(self):
        json_response = self.test_drive(self.test_private_url)

        self.assertTrue(json_response['data']['title'] is not None)
        self.assertTrue(json_response['data']['description'] is not None)
        self.assertEqual(json_response['status'], 200)

    def test_invalid_drive(self):
        json_response = self.test_drive(self.test_invalid_url)

        self.assertTrue(json_response['data']['title'] is not None)
        self.assertTrue(json_response['data']['description'] is not None)
        self.assertTrue(json_response['error_message'] is not None)
        self.assertEqual(json_response['status'], 404)

if __name__ == '__main__':
    unittest.main()

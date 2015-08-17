import unittest

from client import url_utils


class TestValidateImageUrl(unittest.TestCase):

    def test_invalid_url(self):
        domain_url = "https://en.wikipedia.org/"
        image_url = "/static/favicon/wikipedia.ico"
        expected_url = "https://en.wikipedia.org/static/favicon/wikipedia.ico"
        new_image_url = url_utils.validate_image_url(image_url, domain_url)
        self.assertEqual(new_image_url, expected_url)

    def test_invalid_url2(self):
        domain_url = "https://en.wikipedia.org/"
        image_url = "en.wikipedia.org/static/favicon/wikipedia.ico"
        expected_url = "https://en.wikipedia.org/static/favicon/wikipedia.ico"
        new_image_url = url_utils.validate_image_url(image_url, domain_url)
        self.assertEqual(new_image_url, expected_url)

    def test_valid_url(self):
        domain_url = "https://en.wikipedia.org/"
        image_url = "https://en.wikipedia.org/static/favicon/wikipedia.ico"
        expected_url = "https://en.wikipedia.org/static/favicon/wikipedia.ico"
        new_image_url = url_utils.validate_image_url(image_url, domain_url)
        self.assertEqual(new_image_url, expected_url)


if __name__ == '__main__':
    unittest.main()

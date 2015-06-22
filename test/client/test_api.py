from client.api import app
import unittest


class TestApi(unittest.TestCase):

    def test_root_page(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

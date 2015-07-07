import unittest
from client.api import app
import json


class TestDriveMetadata(unittest.TestCase):

    doc_url = "https://docs.google.com/document/d/1FUo-Him4W6qR96_a6Ftx8skefgAe1vHjDPCfUIxtADM/edit"

    def test_drive_metadata(self):
        tester = app.test_client(self)
        response = tester.get('/website?src=' + self.doc_url)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("title"), "Dummy page")
        self.assertEqual(data.get("ownerNames"), ["Samiya Akhtar"])

if __name__ == '__main__':
    unittest.main()

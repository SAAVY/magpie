import unittest

from client import blacklist
from mock import patch, MagicMock


class TestBlacklist(unittest.TestCase):

    def setUp(self):
        current_app = MagicMock()
        current_app.logger = MagicMock()
        self.patcher = patch('client.blacklist.current_app', current_app).start()

    def test_is_inc_request_blacklisted1(self):
        """ test is_inc_request_blacklisted with network mask domain
        """
        blacklist.bl_request_ip = [('127.0.0.0/8', '')]
        self.assertTrue(blacklist.is_inc_request_blacklisted('127.22.234.1'))

    def test_is_inc_request_blacklisted2(self):
        """ test is_inc_request_blacklisted with network ip
        """
        blacklist.bl_request_ip = [('127.0.0.1', '')]
        self.assertTrue(blacklist.is_inc_request_blacklisted('127.0.0.1'))

    def test_is_inc_request_blacklisted3(self):
        """ test is_inc_request_blacklisted with network mask with ip that does not match
        """
        blacklist.bl_request_ip = [('127.0.0.0/24', '')]
        self.assertFalse(blacklist.is_inc_request_blacklisted('127.234.0.1'))

    def test_is_website_blacklisted(self):
        """ test is_website_blacklisted with network mask with ip that does not match
        """
        blacklist.bl_website_ip = [('127.0.0.0/24', '')]
        self.assertTrue(blacklist.is_website_blacklisted('127.0.0.1', '4000'))

    def test_is_website_blacklisted2(self):
        """ test is_website_blacklisted with network mask that does not match
        """
        blacklist.bl_website_ip = [('127.23.0.0/24', '')]
        self.assertFalse(blacklist.is_website_blacklisted('127.0.0.1', '4000'))

    def test_is_website_blacklisted3(self):
        """ test is_website_blacklisted with ip and no port
        """
        blacklist.bl_website_ip = [('192.23.23.1', '')]
        self.assertTrue(blacklist.is_website_blacklisted('192.23.23.1', '4000'))

    def test_is_website_blacklisted4(self):
        """ test is_website_blacklisted with ip and port
        """
        blacklist.bl_website_ip = [('192.23.23.1', '4000')]
        self.assertTrue(blacklist.is_website_blacklisted('192.23.23.1', '4000'))

    def test_is_website_blacklisted5(self):
        """ test is_website_blacklisted with ip and non matching port
        """
        blacklist.bl_website_ip = [('192.23.23.1', '4000')]
        self.assertFalse(blacklist.is_website_blacklisted('192.23.23.1', '4001'))

    def tearDown(self):
        self.patcher.stop()

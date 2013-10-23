import unittest
import em.tests as tests
import requests
from em.libs.routers.identifier import Identifier

class IdentifierTest(unittest.TestCase):

    def test_get_instance(self):
        """
        Make sure the Identifer can parse data out of an HTTPResponse
        object.
        """
        url = "http://www.google.com/"
        response = requests.get(url, timeout=2.5)
        identifier = Identifier.get_instance(url, response)
        self.assertTrue(identifier.parsing_succeeded())
        self.assertIsNotNone(identifier.title())

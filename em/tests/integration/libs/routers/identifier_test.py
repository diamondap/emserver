import unittest
import em.tests as tests
import requests
from em.models import RouterResponse
from em.libs.routers.identifier import Identifier

class IdentifierTest(unittest.TestCase):

    def test_get_instance(self):
        """
        Make sure the Identifer can parse data out of a RouterResponse
        object.
        """
        url = "http://www.google.com/"
        http_response = requests.get(url, timeout=2.5)
        router_response = RouterResponse(
            url=url,
            method='get',
            status_code=http_response.status_code,
            port=RouterResponse.get_port_from_url(url),
            headers=RouterResponse.convert_headers(http_response.headers),
            body=http_response.text)
        identifier = Identifier.get_instance(router_response)
        self.assertTrue(identifier.parsing_succeeded())
        self.assertIsNotNone(identifier.title())

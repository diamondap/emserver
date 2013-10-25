from django.test import TestCase
from em.libs.http import HttpRequest, HttpResponse
from em.libs import utils

class HttpTest(TestCase):

    def setUp(self):
        self.request = HttpRequest(
            url='/relative/url.html',
            method='get',
            headers={'header1': 'value1',
                     'header2': 'value2'},
            data={'data1': 111, 'data2': 222})
        self.response = HttpResponse(
            url='/relative/url.html',
            method='get',
            status_code=200,
            headers={'header1': 'value1',
                     'header2': 'value2'},
            body='<html>')

    def test_request_serialization(self):
        serialized = self.request.to_json()
        deserialized = HttpRequest.from_json(serialized)
        self.assertEqual(self.request.url, deserialized.url)
        self.assertEqual(self.request.method, deserialized.method)
        self.assertEqual(self.request.data, deserialized.data)
        self.assertEqual(self.request.headers, deserialized.headers)
        self.assertIsInstance(deserialized, HttpRequest)

    def test_response_serialization(self):
        serialized = self.response.to_json()
        deserialized = HttpResponse.from_json(serialized)
        self.assertEqual(self.response.url, deserialized.url)
        self.assertEqual(self.response.method, deserialized.method)
        self.assertEqual(self.response.status_code, deserialized.status_code)
        self.assertEqual(self.response.headers, deserialized.headers)
        self.assertEqual(self.response.body, deserialized.body)
        self.assertIsInstance(deserialized, HttpResponse)

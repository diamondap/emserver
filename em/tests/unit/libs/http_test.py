from django.test import TestCase
from em.libs.http import RouterRequest, RouterResponse
from em.libs.json_serializable import list_to_json, list_from_json, to_list
from em.libs import utils

class HttpTest(TestCase):

    def setUp(self):
        pass

    def get_request(self):
        return RouterRequest(
            url='/relative/url.html',
            method='get',
            headers={'header1': 'value1',
                     'header2': 'value2'},
            data={'data1': 111, 'data2': 222})

    def get_response(self):
        return RouterResponse(
            url='/relative/url.html',
            method='get',
            status_code=200,
            headers={'header1': 'value1',
                     'header2': 'value2'},
            body='<html>')


    def test_request_serialization(self):
        request = self.get_request()
        serialized = request.to_json()
        deserialized = RouterRequest.from_json(serialized)
        self.assertEqual(request.url, deserialized.url)
        self.assertEqual(request.method, deserialized.method)
        self.assertEqual(request.data, deserialized.data)
        self.assertEqual(request.headers, deserialized.headers)
        self.assertIsInstance(deserialized, RouterRequest)

    def test_response_serialization(self):
        response = self.get_response()
        serialized = response.to_json()
        deserialized = RouterResponse.from_json(serialized)
        self.assertEqual(response.url, deserialized.url)
        self.assertEqual(response.method, deserialized.method)
        self.assertEqual(response.status_code, deserialized.status_code)
        self.assertEqual(response.headers, deserialized.headers)
        self.assertEqual(response.body, deserialized.body)
        self.assertIsInstance(deserialized, RouterResponse)

    def test_list_to_from_json_request(self):
        r1 = self.get_request()
        r2 = self.get_request()
        request_json = list_to_json([r1, r2])
        requests = list_from_json(request_json, RouterRequest)
        self.assertEqual(r1.url, requests[0].url)
        self.assertEqual(r1.method, requests[0].method)
        self.assertEqual(r1.data, requests[0].data)
        self.assertEqual(r1.headers, requests[0].headers)
        self.assertIsInstance(requests[0], RouterRequest)
        self.assertIsInstance(requests[1], RouterRequest)


    def test_list_to_from_json_response(self):
        r1 = self.get_response()
        r2 = self.get_response()
        response_json = list_to_json([r1, r2])
        responses = list_from_json(response_json, RouterResponse)
        self.assertEqual(r1.url, responses[0].url)
        self.assertEqual(r1.method, responses[0].method)
        self.assertEqual(r1.body, responses[0].body)
        self.assertEqual(r1.headers, responses[0].headers)
        self.assertIsInstance(responses[0], RouterResponse)
        self.assertIsInstance(responses[1], RouterResponse)

    def test_to_list(self):
        r1 = self.get_response()
        r2 = self.get_response()
        responses = to_list([r1, r2])
        self.assertEqual(r1.url, responses[0]['url'])
        self.assertEqual(r1.method, responses[0]['method'])
        self.assertEqual(r1.body, responses[0]['body'])
        self.assertEqual(r1.headers, responses[0]['headers'])
        self.assertIsInstance(responses[0], dict)
        self.assertIsInstance(responses[1], dict)

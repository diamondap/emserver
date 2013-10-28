import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from em import models, tests
from em.libs.routers.identifier import Identifier

class RouterTest(TestCase):

    fixtures = tests.DB_FIXTURES

    def setUp(self):
        pass

    def load(self, fixture):
        prefix = 'routers/medialink/mwn-wapr300n'
        return tests.load_fixture('{0}/{1}'.format(prefix, fixture))

    def test_identify(self):
        html = self.load('login.asp')
        json_data = json.dumps({'body': html, 'port': 80,
                                'url': '/relative.html',
                                'headers': {'header1': 'value1',
                                            'header2': 'value2'}})
        data = {'router_response': json_data}
        client = tests.admin_client()
        response = client.post(reverse('identify_router'), data)
        self.assertEqual(200, response.status_code)

        router = models.Router.objects.first()
        data = json.loads(response.content.decode(encoding='UTF-8'))
        self.assertEqual(router.manufacturer, data['manufacturer'])
        self.assertEqual(router.model, data['model'])
        self.assertEqual(router.firmware_version, data['firmware_version'])
        self.assertEqual(router.auth_protocol, data['auth_protocol'])
        self.assertEqual(router.id, data['id'])

    def test_get_credentials_requests(self):
        client = tests.admin_client()
        data = {'router_id': tests.ROUTER_ID}
        response = client.get(reverse('credentials_request', kwargs=data))
        self.assertEqual(200, response.status_code)

        data = json.loads(response.content.decode(encoding='UTF-8'))
        print(data)
        self.assertEqual(1, len(data))
        self.assertEqual('/login.asp', data[0]['url'])
        self.assertEqual('get', data[0]['method'])
        self.assertTrue('headers' in data[0].keys())
        self.assertTrue('data' in data[0].keys())

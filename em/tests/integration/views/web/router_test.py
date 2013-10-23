from django.test import TestCase
from django.core.urlresolvers import reverse
from em import models, tests

class RouterTest(TestCase):

    fixtures = tests.DB_FIXTURES

    def setUp(self):
        self.data = {'manufacturer': 'EZ-Mart',
                     'model': 'HunkaJunk',
                     'auth_protocol': 'http_basic',
                     'protocol': 'https',
                     'port': '8443',
                     'firmware_version': '2.5.29',
                     'firmware_major': '2',
                     'firmware_minor': '5',
                     'firmware_point': '29',
                     'firmware_date': '12/20/2013',
                     'comments': 'This is test data.'}
        self.args = {'pk': tests.ROUTER_ID}


    def test_index(self):
        client = tests.admin_client()
        response = client.get(reverse('router_index'))
        routers = response.context['data_list']
        self.assertTrue(len(routers) > 0)
        self.assertEqual('MediaLink', routers[0][1])

    def test_detail(self):
        client = tests.admin_client()
        response = client.get(reverse('router_detail', kwargs=self.args))
        router = response.context['router']
        self.assertEqual('MediaLink', router.manufacturer)

    def test_create(self):
        client = tests.admin_client()
        response = client.post(reverse('router_create'), self.data)
        self.assertEqual(303, response.status_code)
        # Make sure our router is there
        router = models.Router.objects.filter(model=self.data['model'])[0]
        self.assertIsNotNone(router)

    def test_edit(self):
        client = tests.admin_client()
        response = client.post(
            reverse('router_edit', kwargs=self.args),
            self.data)
        self.assertEqual(303, response.status_code)
        # Make sure the new name stuck.
        router = models.Router.objects.filter(model=self.data['model']).first()
        self.assertIsNotNone(router)

    def test_delete(self):
        client = tests.admin_client()
        # We do not delete on GET
        response = client.get(reverse('router_delete', kwargs=self.args))
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(
            models.Router.objects.filter(pk=tests.ROUTER_ID).first())
        # But we do delete on POST
        response = client.post(reverse('router_delete', kwargs=self.args))
        self.assertEqual(302, response.status_code)
        self.assertIsNone(
            models.Router.objects.filter(pk=tests.ROUTER_ID).first())

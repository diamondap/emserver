from django.test import TestCase
from django.core.urlresolvers import reverse
from em import models, tests

class RouterPageTest(TestCase):

    fixtures = tests.DB_FIXTURES

    def setUp(self):
        self.data = {'router': tests.ROUTER_ID,
                     'relative_url': '/slash/something/',
                     'title': 'Page Title',
                     'description': 'A router page',
                     'body': '<html>',
                     'comments': 'Listening to Bob Seger'}
        self.args = {'pk': tests.ROUTER_PAGE_ID}

    def test_detail(self):
        client = tests.admin_client()
        response = client.get(reverse('routerpage_detail', kwargs=self.args))
        headers = response.context['headers']
        self.assertEqual(5, len(headers))

    def test_create(self):
        client = tests.admin_client()
        response = client.post(
            reverse('routerpage_create', kwargs={'router': tests.ROUTER_ID}),
            self.data)
        self.assertEqual(303, response.status_code)
        self.assertIsNotNone(models.RouterPage.objects.filter(
                relative_url=self.data['relative_url']).first())

    def test_auto_create(self):
        client = tests.admin_client()
        response = client.post(
            reverse('routerpage_auto_create',
                    kwargs={'router': tests.ROUTER_ID}),
            {'url': 'http://www.google.com'})
        self.assertEqual(303, response.status_code)
        page = models.RouterPage.objects.exclude(
            pk=tests.ROUTER_PAGE_ID).first()
        self.assertIsNotNone(page)
        self.assertTrue(len(list(page.get_headers())) > 1)
        self.assertTrue(len(list(page.get_links())) > 1)

    def test_edit(self):
        client = tests.admin_client()
        response = client.post(reverse('routerpage_edit', kwargs=self.args),
                               self.data)
        self.assertEqual(303, response.status_code)
        self.assertIsNotNone(models.RouterPage.objects.filter(
                relative_url=self.data['relative_url']).first())

    def test_delete(self):
        client = tests.admin_client()
        # We do not delete on GET
        response = client.get(reverse('routerpage_delete', kwargs=self.args))
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(
            models.Router.objects.filter(pk=tests.ROUTER_ID).first())
        # But we do delete on POST
        response = client.post(reverse('routerpage_delete', kwargs=self.args))
        self.assertEqual(302, response.status_code)
        self.assertIsNone(
            models.RouterPage.objects.filter(pk=tests.ROUTER_PAGE_ID).first())

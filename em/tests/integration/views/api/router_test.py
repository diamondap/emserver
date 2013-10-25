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
        identifier = Identifier(
            html=html, url='login.asp', port=80, headers={})
        router = identifier.identify()
        self.assertEqual("MediaLink", router.manufacturer)
        self.assertEqual("MWN-WAPR300N", router.model)
        self.assertEqual("html", router.auth_protocol)
        self.assertEqual(1, router.id)

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

    def test_this(self):
        from django import db
        print(db.connection.settings_dict)
        print(models.Router.objects.count())


    def test_identify(self):
        html = self.load('login.asp')
        identifier = Identifier(
            html=html, url='login.asp', port=80, headers={})
        router = identifier.identify()
        self.assertEqual("MediaLink", router.manufacturer)
        self.assertEqual("MWN-WAPR300N", router.model)
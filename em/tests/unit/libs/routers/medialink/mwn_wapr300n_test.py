from django.test import TestCase
from em.tests import load_fixture
from em.libs import utils
from em.libs.routers.medialink.mwn_wapr300n import Manager

class MwnWapr300NTest(TestCase):

    def setUp(self):
        pass

    def load(self, fixture):
        prefix = 'routers/medialink/mwn-wapr300n'
        return load_fixture('{0}/{1}'.format(prefix, fixture))

    def test_get_login_credentials(self):
        manager = Manager()
        headers = {}
        html = self.load('login.asp')
        (login, password) = manager.get_login_credentials(headers, html)
        self.assertEqual("Homer", login)
        self.assertEqual("FledNanders", password)

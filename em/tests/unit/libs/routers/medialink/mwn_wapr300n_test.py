from django.test import TestCase
from em.tests import load_fixture
from em.libs import utils
from em.libs.http_response import HttpResponse
from em.libs.routers.medialink.mwn_wapr300n import Manager

class MwnWapr300NTest(TestCase):

    def setUp(self):
        pass

    def load(self, fixture):
        prefix = 'routers/medialink/mwn-wapr300n'
        return load_fixture('{0}/{1}'.format(prefix, fixture))

    def test_get_login_credentials(self):
        manager = Manager()
        responses = [HttpResponse(body=self.load('login.asp'))]
        (login, password) = manager.get_login_credentials(responses)
        self.assertEqual("Homer", login)
        self.assertEqual("FledNanders", password)

    def test_get_clients_from_traffic_stats(self):
        manager = Manager()
        response = HttpResponse(body=self.load('updateIptAccount.txt'))
        clients = manager.get_clients_from_traffic_stats(response)
        self.assertEqual(18, len(clients))
        self.assertEqual('192.168.1.102', clients[2]['ip'])
        self.assertEqual('Wireless', clients[2]['conn_type'])
        self.assertEqual('192.168.1.233', clients[17]['ip'])
        self.assertEqual('Wired', clients[17]['conn_type'])

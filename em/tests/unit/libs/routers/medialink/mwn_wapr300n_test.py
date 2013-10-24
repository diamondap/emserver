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
        self.assertEqual('192.168.1.102', clients[2].ip)
        self.assertEqual('wireless', clients[2].conn_type)
        self.assertEqual('192.168.1.233', clients[17].ip)
        self.assertEqual('wired', clients[17].conn_type)

    def test_get_dhcp_clients(self):
        manager = Manager()
        response = HttpResponse(body=self.load('lan_dhcp_clients.asp'))
        clients = manager.get_dhcp_clients(response)
        self.assertEqual(5, len(clients))

        self.assertEqual("", clients[0].hostname)
        self.assertEqual("192.168.1.100", clients[0].ip)
        self.assertEqual("28:EF:01:2B:89:A4", clients[0].mac)

        self.assertEqual("Andrews-iPad", clients[1].hostname)
        self.assertEqual("192.168.1.112", clients[1].ip)
        self.assertEqual("1C:E6:2B:A7:8F:14", clients[1].mac)

        self.assertEqual("android-951c82b7396fc6f7", clients[2].hostname)
        self.assertEqual("192.168.1.110", clients[2].ip)
        self.assertEqual("A0:F4:50:11:E1:74", clients[2].mac)

        self.assertEqual("android_1aa0643d1595227c", clients[3].hostname)
        self.assertEqual("192.168.1.101", clients[3].ip)
        self.assertEqual("10:F9:6F:CD:97:0E", clients[3].mac)

        self.assertEqual("Wii", clients[4].hostname)
        self.assertEqual("192.168.1.103", clients[4].ip)
        self.assertEqual("00:23:31:6B:A9:89", clients[4].mac)

    def test_get_client_list(self):
        manager = Manager()
        # get_client_list() needs to look at responses from two
        # different URLs.
        response1 = HttpResponse(body=self.load('lan_dhcp_clients.asp'),
                                 url='/lan_dhcp_clients.asp')
        response2 = HttpResponse(body=self.load('updateIptAccount.txt'),
                                 url='/updateIptAccount')
        clients = manager.get_client_list([response1, response2])
        self.assertEqual(18, len(clients))

        # 192.168.1.100 Wireless 28:EF:01:2B:89:A4
        self.assertEqual('192.168.1.100', clients[0].ip)
        self.assertEqual('wireless', clients[0].conn_type)
        self.assertEqual('28:EF:01:2B:89:A4', clients[0].mac)

        # 192.168.1.105 Wired None
        self.assertEqual('192.168.1.105', clients[5].ip)
        self.assertEqual('wired', clients[5].conn_type)
        self.assertIsNone(clients[5].mac)

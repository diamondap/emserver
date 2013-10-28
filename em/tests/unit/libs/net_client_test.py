# from django.test import TestCase
# from em.libs.net_client import NetClient
# from em.libs import utils

# class NetClientTest(TestCase):

#     def setUp(self):
#         pass

#     def get_pc_client(self):
#         return NetClient(mac='00:00:00:00:00:00',
#                          ip='1.1.1.1',
#                          hostname='host1',
#                          conn_type='wired',
#                          device_type='pc',
#                          os_type='windows',
#                          is_whitelisted=True,
#                          is_blacklistes=False,
#                          nickname='My PC')

#     def get_ios_client(self):
#         return NetClient(mac='00:00:00:00:00:00',
#                          ip='2.2.2.2',
#                          hostname='host2',
#                          conn_type='wireless',
#                          device_type='tablet',
#                          os_type='ios',
#                          is_whitelisted=False,
#                          is_blacklistes=True,
#                          nickname='My iPad')

#     def get_random_client(self):
#         return NetClient(mac=utils.random_string(),
#                          ip=utils.random_string(),
#                          hostname=utils.random_string(),
#                          conn_type=utils.random_string(),
#                          device_type=utils.random_string(),
#                          os_type=utils.random_string(),
#                          is_whitelisted=utils.random_string(),
#                          is_blacklistes=utils.random_string(),
#                          nickname=utils.random_string())


#     def test_merge(self):
#         client1 = self.get_pc_client()
#         client2 = self.get_ios_client()
#         client2.ip = client1.ip  # must have same IP, or merge won't work
#         client1.merge(client2)
#         self.assertEqual(client1.mac, client2.mac)
#         self.assertEqual(client1.ip, client2.ip)
#         self.assertEqual(client1.hostname, client2.hostname)
#         self.assertEqual(client1.device_type, client2.device_type)
#         self.assertEqual(client1.os_type, client2.os_type)
#         self.assertEqual(client1.is_whitelisted, client2.is_whitelisted)
#         self.assertEqual(client1.is_blacklisted, client2.is_blacklisted)
#         self.assertEqual(client1.nickname, client2.nickname)

#         client3 = self.get_pc_client()
#         client3.ip = '3.3.3.3'
#         with self.assertRaises(ValueError) as ex:
#             client3.merge(client2)

#     def test_merge_lists(self):
#         client1 = self.get_pc_client()
#         client1.mac = '01:01:01:01:01:01'
#         client2 = self.get_ios_client()
#         client2.mac = '02:02:02:02:02:02'
#         client11 = self.get_pc_client()
#         client11.mac = '11:11:11:11:11:11'
#         client11.ip = '1.1.1.1'
#         client22 = self.get_ios_client()
#         client22.ip = '2.2.2.2'
#         client22.mac = '22:22:22:22:22:22'
#         client3 = self.get_random_client()
#         client3.mac = '03:03:03:03:03:03'
#         client4 = self.get_random_client()
#         client4.mac = '04:04:04:04:04:04'
#         list1 = [client1, client2, client3]
#         list2 = [client11, client22, client4]
#         merged = NetClient.merge_lists(list1, list2)


#         # There were 4 unique mac addresses across our
#         # two lists, so we should have four results.
#         self.assertEqual(4, len(merged))

#         # Make sure attributes from list2
#         # overwrote attributes from list1.
#         client = next((c for c in merged if c.ip == '1.1.1.1'))
#         self.assertEqual('11:11:11:11:11:11', client.mac)
#         client = next((c for c in merged if c.ip == '2.2.2.2'))
#         self.assertEqual('22:22:22:22:22:22', client.mac)

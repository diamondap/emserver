import re
from em.libs import utils
from em.libs.net_client import NetClient

# Manager for MediaLink MWN_WAPR300N Router

class Manager:

    manufacturer = 'MediaLink'
    model = 'MWN-WAPR300N'
    parser_type = 'regex'
    comment = ("This router's HTML is unparsable because its data is in "
               "JavaScript variables and it uses document.write everywhere.")
    requests = {
        'Login Credentials': [{'method': 'get', 'url': '/login.asp' }],
        'Client List': [{'method': 'get', 'url': '/lan_dhcp_clients.asp' },
                        {'method': 'get', 'url': '/updateIptAccount' },]
        }

    def __init__(self):
        pass

    def get_login_credentials(self, responses):
        """
        This returns the login name and password from the HTML of the
        login.asp page.

        Param responses is a list of em.libs.HttpResponse objects.

        Returns a tuple: (login, password).
        """
        html = responses[0].body
        login_re = re.compile(r'var username1="(.*)";')
        login = utils.re_first_capture(login_re, html)
        password_re = re.compile(r'var password1="(.*)";')
        password = utils.re_first_capture(password_re, html)
        return (login, password)

    def get_client_list(self, responses):
        dhcp_clients = None
        traffic_clients = None
        for response in responses:
            if 'lan_dhcp_clients.asp' in response.url:
                dhcp_clients = self.get_dhcp_clients(response)
            elif 'updateIptAccount' in response.url:
                traffic_clients = self.get_clients_from_traffic_stats(
                    response)
            else:
                raise ValueError("Unknown URL: {0}".format(response.url))
        assert(dhcp_clients is not None)
        assert(traffic_clients is not None)

        # When we merge NetClient lists, for any items in both lists,
        # attributes from the second list overwrite attributes from
        # the first list. Since the dhcp_clients list has more up-to-date
        # info, we want attributes from that list to win.
        return NetClient.merge_lists(traffic_clients, dhcp_clients)

    # Not part of BaseRouterManager interface
    def get_dhcp_clients(self, response):
        """
        Returns the list of DHCP clients. The return value is a list of
        dictionaries. Each dictionary has keys 'ip' (the device's IP address),
        'mac' (the device's MAC address), and 'hostname' (which will often
        be blank).
        """
        clients = []
        client_re = re.compile(r'var dhcpList=new Array\((.*)\);')
        client_str = utils.re_first_capture(client_re, response.body)
        client_list = client_str.split(',')
        for c in client_list:
            c = c.replace("'", "")
            data = c.split(";")
            clients.append(
                NetClient(hostname=data[0], ip=data[1], mac=data[2]))
        return clients

    def get_clients_from_traffic_stats(self, response):
        """
        The traffic stats page includes a much longer list of IP addresses
        than the DHCP clients page. This is because 1) it may include
        stats on clients that are not currently connected, and 2) it
        includes stats on clients that have static IP addresses.

        The body this response in plain text, not HTML. The return value is
        a list of em.libs.NetClient objects.
        """
        clients = []
        text = response.body
        for line in text.split("\n"):
            line = line.strip()
            data = line.split(';')
            if len(data) == 8:
                clients.append(NetClient(ip=data[0],
                                         conn_type=data[7].lower()))
        return clients

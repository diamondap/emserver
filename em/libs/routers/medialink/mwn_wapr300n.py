import re
from em.libs import utils
from em.libs.base import BaseManager, BaseResponseManager, BaseRequestManager
from em.libs.http import HttpRequest
from em.libs.net_client import NetClient

class Manager(BaseManager):

    def __init__(self):
        BaseManager.__init__(self)
        self.description = 'ResponseManager for MediaLink MWN_WAPR300N Router'
        self.manufacturer = 'MediaLink'
        self.model = 'MWN-WAPR300N'
        self.firmware_version = 'V5.07.42_en_MDL01'
        self.hardware_version = 'V3.0'
        self.parser_type = 'regex'
        self.response_manager = ResponseManager()
        self.request_manager = RequestManager()
        self.comment = """
        This router's HTML is unparsable because its data is in
        JavaScript variables and it uses document.write() everywhere.
        """


class ResponseManager(BaseResponseManager):

    # Map this router's filter type names to our uniform filter type names.
    FILTER_TYPE_MAP = {'allow': 'whitelist',
                       'deny': 'blacklist',
                       'disabled': 'disabled'}

    def __init__(self, *args, **kwargs):
        super(ResponseManager, self).__init__(*args, **kwargs)

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

    def get_filter_type(self, responses):
        """
        This returns the type of MAC filtering that is currently enabled.
        The return value will be one of the following strings, or None if
        we can't determine the filter type.
        - whitelist
        - blacklist
        - disabled
        """
        if not responses:
            raise ValueError('get_filter_type requires a response')
        filter_re = re.compile(r'var filter_mode = "(\w+)";');
        filter_type = utils.re_first_capture(filter_re, responses[0].body)
        return ResponseManager.FILTER_TYPE_MAP.get(filter_type)

    def get_filter_list(self, responses):
        """
        This returns a list of strings. Each string is a MAC address on
        the current black/white list.
        """
        if not responses:
            raise ValueError('get_filter_list requires a response')
        mac_list_re = re.compile(r'var res = "(.*)";');
        mac_list_str = utils.re_first_capture(mac_list_re, responses[0].body)
        return mac_list_str.split(' ')


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


class RequestManager(BaseRequestManager):

    def __init__(self, *args, **kwargs):
        super(RequestManager, self).__init__(*args, **kwargs)

    def get_login_credentials(self):
        """
        Returns a list of requests that the client will need to issue to
        the router to retrieve login credentials. Most routers don't support
        this, because obviously a device should not send you the credentials
        you need to log into it. But this device does, so let's get them.
        """
        return [HttpRequest(method='get', url='/login.asp')]

    def get_login_request(self, responses):
        """
        Returns the request that the client will have to make to the router
        to log in.
        """
        (login, password) = ResponseManager().get_login_credentials(responses)
        data = {'checkEn': 0,
                'Username': login,
                'Password': password}
        return HttpRequest(method='post', url='/LoginCheck', data=data)

    def get_filter_type(self):
        """
        Returns a list of queries the client must issue to the router to get
        the active filter type. Filter types can be 'blacklist', 'whitelist',
        'disabled' or None.
        """
        return [HttpRequest(method='get', url='/wireless_filter.asp')]

    def get_filter_list(self):
        """
        Returns a list of queries the client must issue to the router to get
        the list of MAC addresses that are currently on the black/white list.
        """
        return [HttpRequest(method='get', url='/wireless_filter.asp')]

    def get_client_list(self):
        """
        Returns a list of queries the client must issue to the router to get
        the list of clients currently attached to the network.
        """
        return [HttpRequest(method='get', url='/lan_dhcp_clients.asp'),
                HttpRequest(method='get', url='/updateIptAccount'),]

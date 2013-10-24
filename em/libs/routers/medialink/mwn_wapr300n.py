import re
from em.libs import utils

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

    # responses is a list of hashes
    # each hash has url, method, params, status_code, headers, html

    def __init__(self):
        pass

    def get_login_credentials(self, responses):
        """
        This returns the login name and password from the HTML of the
        login.asp page. Returns a tuple: (login, password).
        """
        html = responses[0].body
        login_re = re.compile(r'var username1="(.*)";')
        login = utils.re_first_capture(login_re, html)
        password_re = re.compile(r'var password1="(.*)";')
        password = utils.re_first_capture(password_re, html)
        return (login, password)

    def get_client_list(self, responses):
        pass


    # Not part of BaseRouterManager interface
    def get_dhcp_clients(self, response):
        pass

    def get_clients_from_traffic_stats(self, response):
        """
        The traffic stats page includes a much longer list of IP addresses
        than the DHCP clients page. This is because 1) it may include
        stats on clients that are not currently connected, and 2) it
        includes stats on clients that have static IP addresses.

        The body this response in plain text, not HTML.
        """
        clients = []
        text = response.body
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            data = line.split(';')
            clients.append({'ip': data[0], 'conn_type': data[7]})
        return clients

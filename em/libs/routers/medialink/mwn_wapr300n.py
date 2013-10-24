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
        'Login Credentials': {'method': 'get', 'url': '/login.asp' },
        }

    def __init__(self):
        pass

    def get_login_credentials(self, headers, html):
        """
        This returns the login name and password from the HTML of the
        login.asp page. Returns a tuple: (login, password)
        """
        login_re = re.compile(r'var username1="(.*)";')
        login = utils.re_first_capture(login_re, html)
        password_re = re.compile(r'var password1="(.*)";')
        password = utils.re_first_capture(password_re, html)
        return (login, password)
